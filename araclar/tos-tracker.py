import difflib
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BOT_VERSIYON = "2.1"

# ── Takip edilen belgeler ────────────────────────────────────────────────────
# "kontrol": belgede kesinlikle geçmesi gereken ifade.
# Bulunamazsa sayfa doğru yüklenmemiş demektir; snapshot alınmaz.

PLATFORMS = [
    {"id": "whatsapp-tos", "platform": "WhatsApp", "belge": "Hizmet Şartları",
     "url": "https://www.whatsapp.com/legal/terms-of-service",
     "kontrol": "Hizmet Koşulları"},

    {"id": "whatsapp-privacy", "platform": "WhatsApp", "belge": "Gizlilik Politikası",
     "url": "https://www.whatsapp.com/legal/privacy-policy",
     "kontrol": "Topladığımız Bilgiler"},

    {"id": "whatsapp-cookies", "platform": "WhatsApp", "belge": "Çerez Politikası",
     "url": "https://www.whatsapp.com/legal/cookies",
     "kontrol": "çerez"},

    {"id": "bip-kullanim", "platform": "BiP", "belge": "Kullanım Koşulları",
     "url": "https://bip.com/tr/kullanim-kosullari/",
     "kontrol": "Turkcell"},

    {"id": "signal-legal", "platform": "Signal", "belge": "Hizmet Şartları ve Gizlilik",
     "url": "https://signal.org/legal/",
     "kontrol": "Signal"},

    {"id": "offsec-tos", "platform": "OffSec", "belge": "Terms and Conditions",
     "url": "https://offsec.com/legal-docs/",
     "kontrol": "OffSec"},

    {"id": "offsec-privacy", "platform": "OffSec", "belge": "Privacy Notice",
     "url": "https://www.offsec.com/legal/privacy-policy/",
     "kontrol": "privacy"},
]

# JavaScript ile yüklendiği için takip edilemeyenler (bkz. TAKIP-DURUMU.md):
#   BiP Aydınlatma Metni, Trendyol Üyelik/KVKK/Çerez
#   Playwright entegrasyonu sonrası eklenecek.

HASHES_FILE = Path("araclar/hashes.json")
SNAPSHOT_DIR = Path("araclar/snapshots")

HEADERS = {
    "User-Agent": (
        f"Mozilla/5.0 (compatible; OkumadinBot/{BOT_VERSIYON}; "
        "+https://github.com/mVonal/Okumadin)"
    ),
    "Accept-Language": "tr-TR,tr;q=0.9,en;q=0.5",
}

# ── OKM Taxonomy anahtar kelimeleri ──────────────────────────────────────────

TAXONOMY_ANAHTARLARI = {
    "DATA_TRANSFER": ["yurt dışı", "aktarım", "transfer", "cross-border",
                      "international", "sunucu", "veri merkezi", "data center"],
    "THIRD_PARTY": ["üçüncü taraf", "third party", "iş ortağı", "partner",
                    "hizmet sağlayıcı", "service provider", "paylaş", "share"],
    "METADATA": ["metadata", "kullanım bilgi", "log", "kayıt bilgi",
                 "usage information", "cihaz bilgi", "device information"],
    "CONSENT": ["açık rıza", "onay", "consent", "izin", "opt-in", "opt-out"],
    "COOKIES": ["çerez", "cookie", "izleyici", "tracker", "piksel", "pixel"],
    "RETENTION": ["saklama", "retention", "silme", "imha", "delete", "muhafaza"],
    "GOVERNING_LAW": ["geçerli hukuk", "governing law", "tabi", "yasalar"],
    "JURISDICTION": ["mahkeme", "yetkili", "court", "jurisdiction", "tahkim",
                     "arbitration", "uyuşmazlık", "dispute"],
    "AI_USAGE": ["yapay zeka", "artificial intelligence", "machine learning",
                 "model eğitim", "training", " ai "],
    "CHILDREN": ["çocuk", "children", "reşit", "minor", "yaş sınır"],
    "PROFILING": ["profil", "profiling", "hedefleme", "targeting", "reklam",
                  "advertis", "kişiselleştir", "personaliz"],
    "ACCOUNT_DELETION": ["hesap silme", "hesabınızı sil", "delete your account",
                         "kapatma", "termination", "fesih"],
    "CLOUD_BACKUP": ["yedek", "backup", "icloud", "google drive", "bulut"],
    "LAW_ENFORCEMENT": ["kolluk", "law enforcement", "mahkeme kararı",
                        "devlet talep", "government request", "yasal talep",
                        "resmi makam", "yetkili makam"],
}

GURULTU_KALIPLARI = [
    r"^\s*$",
    r"^\d{1,2}[./]\d{1,2}[./]\d{4}$",
    r"^(copyright|©).*$",
    r"^[\d\s.,:-]+$",
]

MIN_ANLAMLI_UZUNLUK = 40
MIN_SAYFA_UZUNLUK = 1000


# ── Metin temizleme ve çekme ─────────────────────────────────────────────────

def temizle_metin(html: str) -> str:
    """HTML'den dinamik ve anlamsız içeriği ayıklayıp saf metin döner."""
    soup = BeautifulSoup(html, "html.parser")

    for etiket in soup(["script", "style", "noscript", "iframe",
                        "svg", "meta", "link"]):
        etiket.decompose()

    satirlar = []
    for satir in soup.get_text(separator="\n").splitlines():
        satir = re.sub(r"\s+", " ", satir.strip())
        if satir:
            satirlar.append(satir)

    return "\n".join(satirlar)


def sayfa_cek(url: str, bekleme: float = 3.0) -> str | None:
    """Sayfayı iki kez çeker, yalnızca her iki çekimde de bulunan
    satırları döner. Dönen banner, reklam, zaman damgası gibi dinamik
    içerik böylece elenir — siteye özel kural gerekmez."""
    metinler = []

    for i in range(2):
        try:
            r = requests.get(url, headers=HEADERS, timeout=30)
            r.raise_for_status()
            metinler.append(temizle_metin(r.text))
        except Exception as e:
            print(f"  HATA: {url} çekilemedi — {e}")
            return None
        if i == 0:
            time.sleep(bekleme)

    ikinci = set(metinler[1].splitlines())
    kararli = [s for s in metinler[0].splitlines() if s in ikinci]

    atilan = len(metinler[0].splitlines()) - len(kararli)
    if atilan > 0:
        print(f"  {atilan} dinamik satır elendi")

    return "\n".join(kararli)


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ── Snapshot yönetimi ────────────────────────────────────────────────────────

def snapshot_oku(pid: str) -> str | None:
    yol = SNAPSHOT_DIR / f"{pid}.txt"
    return yol.read_text(encoding="utf-8") if yol.exists() else None


def snapshot_yaz(pid: str, metin: str) -> None:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    (SNAPSHOT_DIR / f"{pid}.txt").write_text(metin, encoding="utf-8")


# ── Diff ve sınıflandırma ────────────────────────────────────────────────────

def gurultu_mu(satir: str) -> bool:
    icerik = satir[1:].strip()
    if len(icerik) < MIN_ANLAMLI_UZUNLUK:
        return True
    return any(re.match(k, icerik, re.IGNORECASE) for k in GURULTU_KALIPLARI)


def diff_cikar(eski: str, yeni: str) -> tuple[list[str], list[str]]:
    diff = difflib.unified_diff(
        eski.splitlines(), yeni.splitlines(), lineterm="", n=0
    )

    eklenen, silinen = [], []
    for satir in diff:
        if satir.startswith(("+++", "---")):
            continue
        if satir.startswith("+") and not gurultu_mu(satir):
            eklenen.append(satir[1:].strip())
        elif satir.startswith("-") and not gurultu_mu(satir):
            silinen.append(satir[1:].strip())

    return eklenen, silinen


def taxonomy_eslestir(satirlar: list[str]) -> list[str]:
    birlesik = " ".join(satirlar).lower()
    return [k for k, anahtarlar in TAXONOMY_ANAHTARLARI.items()
            if any(a.lower() in birlesik for a in anahtarlar)]


# ── GitHub issue yönetimi ────────────────────────────────────────────────────

def acik_issue_var_mi(baslik: str) -> bool:
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not token or not repo:
        return False

    try:
        resp = requests.get(
            f"https://api.github.com/repos/{repo}/issues",
            headers={"Authorization": f"Bearer {token}",
                     "Accept": "application/vnd.github+json"},
            params={"state": "open", "labels": "tos-degisikligi",
                    "per_page": 100},
            timeout=15,
        )
        if resp.status_code != 200:
            return False
        return any(i.get("title") == baslik for i in resp.json())
    except Exception:
        return False


def issue_ac(platform: dict, eklenen: list[str], silinen: list[str],
             kategoriler: list[str]) -> None:
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not token or not repo:
        print("  GitHub token yok — issue açılamadı")
        return

    baslik = f"[ToS Değişikliği] {platform['platform']} — {platform['belge']}"

    if acik_issue_var_mi(baslik):
        print("  Bu belge için zaten açık issue var — yenisi açılmadı")
        return

    tarih = datetime.now(timezone.utc).strftime("%d.%m.%Y")

    def blok(ust_baslik: str, satirlar: list[str], limit: int = 15) -> str:
        if not satirlar:
            return ""
        gosterilecek = satirlar[:limit]
        fazla = len(satirlar) - len(gosterilecek)
        icerik = "\n".join(f"- {s}" for s in gosterilecek)
        if fazla > 0:
            icerik += f"\n- _(+{fazla} satır daha)_"
        return f"### {ust_baslik}\n{icerik}\n\n"

    kategori_metni = (", ".join(f"`{k}`" for k in kategoriler)
                      if kategoriler
                      else "_Taxonomy eşleşmesi yok — genel değişiklik_")

    govde = (
        f"**Platform:** {platform['platform']}\n"
        f"**Belge:** {platform['belge']}\n"
        f"**URL:** {platform['url']}\n"
        f"**Tespit tarihi:** {tarih}\n\n"
        f"**Etkilenen OKM kategorileri:** {kategori_metni}\n\n"
        f"---\n\n"
        + blok("Eklenen ifadeler", eklenen)
        + blok("Çıkarılan ifadeler", silinen)
        + "---\n\n"
        f"### Yapılacaklar\n"
        f"- [ ] Değişikliğin analizi etkileyip etkilemediğine karar ver\n"
        f"- [ ] Etkiliyorsa ilgili bulguyu güncelle\n"
        f"- [ ] OKM Score'u yeniden hesapla\n"
        f"- [ ] `degisiklik-log.md` dosyasına işle\n"
        f"- [ ] Yayın geçidini uygula\n"
        f"- [ ] İçerik üretimi planla (değişiklik haberi)\n\n"
        f"---\n"
        f"*Okumadın ToS takip botu v{BOT_VERSIYON} tarafından otomatik açıldı. "
        f"Karar insana aittir (Anayasa m.7).*"
    )

    resp = requests.post(
        f"https://api.github.com/repos/{repo}/issues",
        headers={"Authorization": f"Bearer {token}",
                 "Accept": "application/vnd.github+json"},
        json={"title": baslik, "body": govde, "labels": ["tos-degisikligi"]},
        timeout=15,
    )

    if resp.status_code == 201:
        print(f"  Issue açıldı: {resp.json().get('html_url')}")
    else:
        print(f"  Issue açılamadı: {resp.status_code}")


# ── Ana akış ─────────────────────────────────────────────────────────────────

def hashes_oku() -> dict:
    if HASHES_FILE.exists():
        return json.loads(HASHES_FILE.read_text(encoding="utf-8"))
    return {}


def hashes_yaz(veri: dict) -> None:
    HASHES_FILE.parent.mkdir(parents=True, exist_ok=True)
    HASHES_FILE.write_text(
        json.dumps(veri, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def main() -> None:
    zaman = datetime.now(timezone.utc)
    print(f"Okumadın ToS Takip Botu v{BOT_VERSIYON} — {zaman.isoformat()}\n")

    hashes = hashes_oku()
    anlamli = 0
    gurultu = 0
    atlanan = 0

    for platform in PLATFORMS:
        pid = platform["id"]
        print(f"{platform['platform']} / {platform['belge']}")

        yeni_metin = sayfa_cek(platform["url"])

        if yeni_metin is None:
            print("  Atlandı (erişim hatası)\n")
            atlanan += 1
            continue

        kontrol = platform.get("kontrol")
        if kontrol and kontrol.lower() not in yeni_metin.lower():
            print(f"  UYARI: Beklenen içerik bulunamadı ('{kontrol}')")
            print("  Muhtemelen JavaScript ile yükleniyor — snapshot alınmadı\n")
            atlanan += 1
            continue

        if len(yeni_metin) < MIN_SAYFA_UZUNLUK:
            print(f"  UYARI: İçerik şüpheli kısa ({len(yeni_metin)} karakter)")
            print("  Snapshot alınmadı\n")
            atlanan += 1
            continue

        yeni_hash = sha256(yeni_metin)
        eski_hash = hashes.get(pid, {}).get("hash")
        eski_metin = snapshot_oku(pid)

        if eski_hash is None or eski_metin is None:
            print("  İlk kayıt — snapshot oluşturuldu")
            snapshot_yaz(pid, yeni_metin)

        elif yeni_hash != eski_hash:
            eklenen, silinen = diff_cikar(eski_metin, yeni_metin)

            if not eklenen and not silinen:
                print("  Değişiklik var ama anlamsız (gürültü) — issue açılmadı")
                gurultu += 1
            else:
                kategoriler = taxonomy_eslestir(eklenen + silinen)
                print(f"  ANLAMLI DEĞİŞİKLİK: +{len(eklenen)} / -{len(silinen)} satır")
                if kategoriler:
                    print(f"  Kategoriler: {', '.join(kategoriler)}")
                issue_ac(platform, eklenen, silinen, kategoriler)
                anlamli += 1

            snapshot_yaz(pid, yeni_metin)

        else:
            print("  Değişiklik yok")

        hashes[pid] = {
            "platform": platform["platform"],
            "belge": platform["belge"],
            "url": platform["url"],
            "hash": yeni_hash,
            "son_kontrol": zaman.isoformat(),
        }
        print()

    hashes_yaz(hashes)
    print(f"Tamamlandı. Anlamlı: {anlamli} · Gürültü: {gurultu} · "
          f"Atlanan: {atlanan}")


if __name__ == "__main__":
    main()
