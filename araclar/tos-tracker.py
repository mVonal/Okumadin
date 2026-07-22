import difflib
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# ── Takip edilen belgeler ────────────────────────────────────────────────────

PLATFORMS = [
    {"id": "whatsapp-tos", "platform": "WhatsApp", "belge": "Hizmet Şartları",
     "url": "https://www.whatsapp.com/legal/terms-of-service",
     "kontrol": "Limitation of Liability"},
    {"id": "whatsapp-privacy", "platform": "WhatsApp", "belge": "Gizlilik Politikası",
     "url": "https://www.whatsapp.com/legal/privacy-policy",
     "kontrol": "Topladığımız Bilgiler"},
    {"id": "whatsapp-cookies", "platform": "WhatsApp", "belge": "Çerez Politikası",
     "url": "https://www.whatsapp.com/legal/cookies",
     "kontrol": "cookie"},
    {"id": "bip-gizlilik", "platform": "BiP", "belge": "Aydınlatma Metni",
     "url": "https://bip.com/tr/gizlilik-politikasi/",
     "kontrol": "kişisel veri"},
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

HASHES_FILE = Path("araclar/hashes.json")
SNAPSHOT_DIR = Path("araclar/snapshots")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; OkumadinBot/2.0; "
        "+https://github.com/mVonal/Okumadin)"
    )
}

# ── OKM Taxonomy anahtar kelimeleri ──────────────────────────────────────────
# Değişen metin bu kelimeleri içeriyorsa ilgili kategori tetiklenir.

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

# Anlamsız kabul edilen değişiklikler (yalnızca bunlar varsa issue açılmaz)
GURULTU_KALIPLARI = [
    r"^\s*$",                      # boş satır
    r"^\d{1,2}[./]\d{1,2}[./]\d{4}$",  # yalnızca tarih
    r"^(copyright|©).*$",
    r"^[\d\s.,:-]+$",              # yalnızca sayı ve noktalama
]

MIN_ANLAMLI_UZUNLUK = 40  # bu karakterden kısa değişiklikler gürültü sayılır


# ── Metin temizleme ──────────────────────────────────────────────────────────

def temizle_metin(html: str) -> str:
    """HTML'den dinamik ve anlamsız içeriği ayıklayıp saf metin döner."""
    soup = BeautifulSoup(html, "html.parser")

    # Dinamik içerik üreten etiketleri tamamen kaldır
    for etiket in soup(["script", "style", "noscript", "iframe",
                        "svg", "meta", "link"]):
        etiket.decompose()

    metin = soup.get_text(separator="\n")

    # Satır bazında normalize et
    satirlar = []
    for satir in metin.splitlines():
        satir = satir.strip()
        satir = re.sub(r"\s+", " ", satir)
        if satir:
            satirlar.append(satir)

    return "\n".join(satirlar)


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ── Ağdan çekme ──────────────────────────────────────────────────────────────

def sayfa_cek(url: str) -> str | None:
    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        return temizle_metin(r.text)
    except Exception as e:
        print(f"  HATA: {url} çekilemedi — {e}")
        return None


# ── Snapshot yönetimi ────────────────────────────────────────────────────────

def snapshot_oku(pid: str) -> str | None:
    yol = SNAPSHOT_DIR / f"{pid}.txt"
    return yol.read_text(encoding="utf-8") if yol.exists() else None


def snapshot_yaz(pid: str, metin: str) -> None:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    (SNAPSHOT_DIR / f"{pid}.txt").write_text(metin, encoding="utf-8")


# ── Diff ve sınıflandırma ────────────────────────────────────────────────────

def gurultu_mu(satir: str) -> bool:
    """Bu satır anlamsız bir değişiklik mi?"""
    icerik = satir[1:].strip()  # baştaki +/- işaretini at
    if len(icerik) < MIN_ANLAMLI_UZUNLUK:
        return True
    for kalip in GURULTU_KALIPLARI:
        if re.match(kalip, icerik, re.IGNORECASE):
            return True
    return False


def diff_cikar(eski: str, yeni: str) -> tuple[list[str], list[str]]:
    """Anlamlı eklenen ve silinen satırları döner."""
    diff = difflib.unified_diff(
        eski.splitlines(), yeni.splitlines(), lineterm="", n=0
    )

    eklenen, silinen = [], []
    for satir in diff:
        if satir.startswith("+++") or satir.startswith("---"):
            continue
        if satir.startswith("+") and not gurultu_mu(satir):
            eklenen.append(satir[1:].strip())
        elif satir.startswith("-") and not gurultu_mu(satir):
            silinen.append(satir[1:].strip())

    return eklenen, silinen


def taxonomy_eslestir(satirlar: list[str]) -> list[str]:
    """Değişen metnin hangi OKM kategorilerini ilgilendirdiğini bulur."""
    birlesik = " ".join(satirlar).lower()
    eslesenler = []
    for kategori, anahtarlar in TAXONOMY_ANAHTARLARI.items():
        if any(a.lower() in birlesik for a in anahtarlar):
            eslesenler.append(kategori)
    return eslesenler


# ── GitHub issue yönetimi ────────────────────────────────────────────────────

def acik_issue_var_mi(baslik: str) -> bool:
    """Aynı başlıkta açık bir issue zaten var mı?"""
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not token or not repo:
        return False

    try:
        resp = requests.get(
            f"https://api.github.com/repos/{repo}/issues",
            headers={"Authorization": f"Bearer {token}",
                     "Accept": "application/vnd.github+json"},
            params={"state": "open", "labels": "tos-degisikligi", "per_page": 100},
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

    def blok(baslik_metni: str, satirlar: list[str], limit: int = 15) -> str:
        if not satirlar:
            return ""
        gosterilecek = satirlar[:limit]
        fazla = len(satirlar) - len(gosterilecek)
        icerik = "\n".join(f"- {s}" for s in gosterilecek)
        if fazla > 0:
            icerik += f"\n- _(+{fazla} satır daha)_"
        return f"### {baslik_metni}\n{icerik}\n\n"

    kategori_metni = (
        ", ".join(f"`{k}`" for k in kategoriler) if kategoriler
        else "_Taxonomy eşleşmesi yok — genel değişiklik_"
    )

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
        f"*Okumadın ToS takip botu tarafından otomatik açıldı. "
        f"Karar insana aittir (Anayasa m.7).*"
    )

    resp = requests.post(
        f"https://api.github.com/repos/{repo}/issues",
        headers={"Authorization": f"Bearer {token}",
                 "Accept": "application/vnd.github+json"},
        json={"title": baslik, "body": govde,
              "labels": ["tos-degisikligi"]},
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
    print(f"Okumadın ToS Takip Botu v2.0 — {zaman.isoformat()}\n")

    hashes = hashes_oku()
    anlamli_degisiklik = 0
    gurultu_degisiklik = 0

    for platform in PLATFORMS:
        pid = platform["id"]
        print(f"{platform['platform']} / {platform['belge']}")

        yeni_metin = sayfa_cek(platform["url"])
        if yeni_metin is None:
            print("  Atlandı\n")
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
                gurultu_degisiklik += 1
            else:
                kategoriler = taxonomy_eslestir(eklenen + silinen)
                print(f"  ANLAMLI DEĞİŞİKLİK: "
                      f"+{len(eklenen)} / -{len(silinen)} satır")
                if kategoriler:
                    print(f"  Kategoriler: {', '.join(kategoriler)}")
                issue_ac(platform, eklenen, silinen, kategoriler)
                anlamli_degisiklik += 1

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
    print(f"Tamamlandı. Anlamlı: {anlamli_degisiklik} · "
          f"Gürültü (yok sayıldı): {gurultu_degisiklik}")


if __name__ == "__main__":
    main()
