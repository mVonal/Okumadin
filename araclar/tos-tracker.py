import hashlib
import json
import os
import sys
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

# Takip edilecek platformlar ve sayfalar
PLATFORMS = [
    {
        "id": "whatsapp-tos",
        "platform": "WhatsApp",
        "belge": "Hizmet Şartları",
        "url": "https://www.whatsapp.com/legal/terms-of-service",
        "selector": "body",
    },
    {
        "id": "whatsapp-privacy",
        "platform": "WhatsApp",
        "belge": "Gizlilik Politikası",
        "url": "https://www.whatsapp.com/legal/privacy-policy",
        "selector": "body",
    },
    {
        "id": "whatsapp-cookies",
        "platform": "WhatsApp",
        "belge": "Çerez Politikası",
        "url": "https://www.whatsapp.com/legal/cookies",
        "selector": "body",
    },
    {
        "id": "bip-gizlilik",
        "platform": "BiP",
        "belge": "Aydınlatma Metni",
        "url": "https://bip.com/tr/gizlilik-politikasi/",
        "selector": "body",
    },
    {
        "id": "bip-kullanim",
        "platform": "BiP",
        "belge": "Kullanım Koşulları",
        "url": "https://bip.com/tr/kullanim-kosullari/",
        "selector": "body",
    },
    {
        "id": "signal-legal",
        "platform": "Signal",
        "belge": "Hizmet Şartları ve Gizlilik Politikası",
        "url": "https://signal.org/legal/",
        "selector": "body",
    },
    {
        "id": "trendyol-uyelik",
        "platform": "Trendyol",
        "belge": "Üyelik Sözleşmesi",
        "url": "https://www.trendyol.com/s/alici-uyelik-sozlesmesi",
        "selector": "body",
    },
    {
        "id": "trendyol-kvkk",
        "platform": "Trendyol",
        "belge": "Aydınlatma Metni",
        "url": "https://www.trendyol.com/kisisel_verilerin_korunmasi",
        "selector": "body",
    },
]

HASHES_FILE = "araclar/hashes.json"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; OkumadinBot/1.0; "
        "+https://github.com/okumadin)"
    )
}


def fetch_page(url: str, selector: str) -> str | None:
    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        element = soup.select_one(selector)
        return element.get_text(separator=" ", strip=True) if element else None
    except Exception as e:
        print(f"HATA: {url} çekilemedi — {e}")
        return None


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_hashes() -> dict:
    if os.path.exists(HASHES_FILE):
        with open(HASHES_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_hashes(hashes: dict) -> None:
    os.makedirs("araclar", exist_ok=True)
    with open(HASHES_FILE, "w", encoding="utf-8") as f:
        json.dump(hashes, f, ensure_ascii=False, indent=2)


def open_github_issue(platform: str, belge: str, url: str) -> None:
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not token or not repo:
        print("GitHub token veya repo bilgisi eksik — issue açılamadı")
        return

    tarih = datetime.now(timezone.utc).strftime("%d.%m.%Y")
    baslik = f"[ToS Değişikliği] {platform} — {belge}"
    govde = (
        f"## Otomatik Tespit\n\n"
        f"**Platform:** {platform}\n"
        f"**Belge:** {belge}\n"
        f"**URL:** {url}\n"
        f"**Tespit tarihi:** {tarih}\n\n"
        f"Bu sayfa bir önceki kontrol ile kıyaslandığında "
        f"içerik değişikliği tespit edildi.\n\n"
        f"### Yapılacaklar\n"
        f"- [ ] Sayfayı inceleyip ne değiştiğini belirle\n"
        f"- [ ] Analiz dosyasını güncelle\n"
        f"- [ ] Değişiklik log'una ekle\n"
        f"- [ ] Sosyal medya içeriği planla\n\n"
        f"---\n"
        f"*Bu issue okumadin ToS takip botu tarafından otomatik açıldı.*"
    )

    api_url = f"https://api.github.com/repos/{repo}/issues"
    resp = requests.post(
        api_url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        },
        json={"title": baslik, "body": govde, "labels": ["tos-degisikligi"]},
        timeout=15,
    )

    if resp.status_code == 201:
        print(f"  Issue açıldı: {resp.json().get('html_url')}")
    else:
        print(f"  Issue açılamadı: {resp.status_code} — {resp.text}")


def main() -> None:
    print(f"ToS Takip Botu başlatıldı — {datetime.now(timezone.utc).isoformat()}\n")
    hashes = load_hashes()
    degisiklik_sayisi = 0

    for platform in PLATFORMS:
        pid = platform["id"]
        print(f"Kontrol ediliyor: {platform['platform']} / {platform['belge']}")

        icerik = fetch_page(platform["url"], platform["selector"])
        if icerik is None:
            print("  Atlandı (erişim hatası)\n")
            continue

        yeni_hash = sha256(icerik)
        eski_hash = hashes.get(pid, {}).get("hash")

        if eski_hash is None:
            print("  İlk kayıt — hash kaydedildi")
        elif yeni_hash != eski_hash:
            print(f"  DEĞİŞİKLİK TESPİT EDİLDİ!")
            degisiklik_sayisi += 1
            open_github_issue(
                platform["platform"],
                platform["belge"],
                platform["url"],
            )
        else:
            print("  Değişiklik yok")

        hashes[pid] = {
            "platform": platform["platform"],
            "belge": platform["belge"],
            "url": platform["url"],
            "hash": yeni_hash,
            "son_kontrol": datetime.now(timezone.utc).isoformat(),
        }
        print()

    save_hashes(hashes)
    print(f"Tamamlandı. {degisiklik_sayisi} değişiklik tespit edildi.")

    if degisiklik_sayisi > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
