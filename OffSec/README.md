# OffSec (Offensive Security) — Hizmet Şartları ve Gizlilik Analizi

**Şirket:** OffSec Services LLC
**Merkez:** 230 Park Avenue, New York, NY 10169, ABD
**Platform:** offsec.com
**Ürünler:** PEN-200/OSCP ve diğer sertifikasyon kursları
**Analiz tarihi:** 24.04.2026
**Kaynaklar:**
- https://www.offsec.com/legal/privacy-policy/
- https://offsec.com/legal-docs/
- https://offsec.com/cookie-policy/

> Bu analiz yalnızca bilgilendirme amaçlıdır, hukuki tavsiye niteliği
> taşımaz. Tüm tespitler OffSec'in kendi yayımladığı belgelere ve
> kamuya açık kaynaklara dayanmaktadır.

---

## Neden Bu Platform Analiz Edildi?

OffSec, dünyada en tanınan siber güvenlik sertifikasyon
platformlarından biridir. OSCP başta olmak üzere OffSec
sertifikaları Türkiye'deki siber güvenlik profesyonelleri
için fiilen bir sektör standardına dönüşmüştür.

Bu platformu kullanan kişiler genellikle veri güvenliği
konusunda bilinçli bireylerdir — tam da bu yüzden bu analiz
değerlidir. Firewall'larınız, EDR'ınız ve IDS/IPS sistemleriniz
ne kadar güçlü olursa olsun hukuksal zemine oturtulmuş
veri aktarımlarını engelleyemezler. Çünkü siz bizzat onayladınız.

---

## ÖZ

**Tek cümle:** OffSec bir ABD şirketi — sınav webcam
kayıtlarınız ABD'de saklanıyor, işvereniniz eğitiminizi
finanse ettiyse sınav sonuçlarınıza erişebiliyor ve
sertifika bilgileriniz kamuya açık veritabanında görünüyor.

**En kritik 3 madde:**
1. İşvereniniz ödediyse hesabınız işveren kontrolüne girer,
   tüm sınav verileri işverenle paylaşılır
2. Sertifika sahiplerinin isim, uzmanlık ve sınav bilgileri
   kamuya açık kayıtta — savunma ve kritik altyapı
   çalışanları için OPSEC riski
3. ToS, sınav davranış verisi ve webcam kayıtlarının
   AI eğitiminde kullanılamayacağına dair güvence içermiyor

**Risk skoru:** 🟠 7/10

---

## Kabul Ettiğiniz Belgeler

| Belge | Kabul Yöntemi |
|---|---|
| Terms and Conditions | Satın alma veya kullanıma devam |
| Privacy Notice | Siteye giriş veya ürün kullanımı |
| Academic Policy | Sınava kayıt |
| Exam Guides | Sınava giriş |
| Proctoring Guidelines | Sınava giriş |
| Cookie Policy | Siteyi ziyaret |

---

## Skorlar

| Kriter | Alt Skor | Ağırlık |
|---|---|---|
| Yurt dışı veri aktarımı | 8 / 10 | %20 |
| Üçüncü taraf paylaşımı | 6 / 10 | %15 |
| Metadata/veri toplama kapsamı | 7 / 10 | %15 |
| KVKK uyumu | 8 / 10 | %20 |
| Belge şeffaflığı ve erişilebilirliği | 5 / 10 | %15 |
| Yetkili hukuk ve mahkeme | 7 / 10 | %15 |
| **Genel risk skoru** | **🟠 7 / 10** | |

**Bağlam notu:** Bu skor diğer platformlarla aynı metodoloji
ile hesaplanmıştır. OffSec bir mesajlaşma uygulaması veya
e-ticaret platformu değil, profesyonel bir eğitim ve
sertifikasyon platformudur. Sınav proctoring gibi bazı
veri işleme uygulamaları hizmetin doğasından kaynaklanmaktadır.
Ancak bu durum diğer bulguları geçersiz kılmaz.

---

## 🔴 Kırmızı Bayraklar

### 1. Sınav Sırasında Webcam ve Ekran Kaydı Alınıyor

Terms and Conditions'a göre sınavlar webcam ve ekran kaydı
ile proctoring yapılmaktadır. Privacy Notice'a göre bu video
kayıtları saklanmaktadır. Kayıtların ne kadar süre
saklandığı, kimlerle paylaşılabileceği ve nasıl imha
edildiği açıkça belirtilmemiştir.

Privacy Notice ayrıca şunu belirtmektedir: bu kayıtlar,
webcam açısına giren ya da ekranda görülen **üçüncü taraf
kişisel verilerini** de içerebilir.

**Kaynak:** Privacy Notice "Exam Proctoring" bölümü ·
Terms and Conditions sınav koşulları

---

### 2. Şirketiniz Verilerinizi Kontrol Edebilir

Terms and Conditions'ın "Customer User" maddesine göre
eğitiminiz için işvereniniz veya başka bir üçüncü taraf
ödeme yapmışsa:

- Hesabınız işverenin kontrolüne girer
- Kişisel verileriniz işverenle ve yöneticileriyle paylaşılır
- Verileriniz işverenin diğer kullanıcılarına görünür olabilir
- OffSec, e-posta domaininize sahip şirkete hesabınızı
  devredebilir

Bir Türk şirketinin çalışanı olarak OffSec eğitimi alıyor
ve masrafları şirketiniz karşılıyorsa sınav sonuçlarınız
dahil tüm kişisel verileriniz işvereninizin erişimine
açık hale gelir.

**Kaynak:** Terms and Conditions "Customer User" maddeleri (a), (b), (c)

---

### 3. Sertifika Sahiplerinin Kimlik Bilgileri Kamuya Açık

Terms and Conditions'ın "Public Register" maddesine göre
OffSec, sertifika sahiplerine ilişkin kamuya açık bir
kayıt tutma hakkını saklı tutmaktadır. Bu kayıt şunları içerir:

- Öğrenci adı ve soyadı
- OSID (Offensive Security Identification Number)
- Alınan kurs
- Geçilen sınav
- Sertifika verilme **ve iptal** durumu

Bu bilgiler ayrıca sizin için ödeme yapan herhangi bir
üçüncü tarafa da iletilebilir.

**OPSEC boyutu:** Türkiye'de savunma, istihbarat veya kritik
altyapı alanlarında çalışan kişilerin ofansif siber güvenlik
sertifikasyon bilgileri, herhangi bir üçüncü tarafça
erişilebilir kamuya açık bir veritabanında yer almaktadır.
Bir ülkenin ofansif siber güvenlik kapasitesine sahip
bireylerinin kimliği ve uzmanlık alanları bu yolla
haritalanabilir durumdadır.

**Kaynak:** Terms and Conditions "Public Register" maddesi

---

### 4. Türkiye ABD Veri Koruma Kapsamı Dışında

OffSec Services LLC bir ABD şirketidir. Privacy Notice GDPR
kapsamını referans almaktadır. Türkiye EEA dışında kaldığından
Türk kullanıcılar GDPR korumalarından tam olarak yararlanamaz.

OffSec'in kendi belgelerinde KVKK'ya hiçbir atıf
yapılmamaktadır. ABD'nin CLOUD Act (2018) yasası kapsamında
Amerikan mahkemeleri, OffSec'in Türk kullanıcılara ait
verilerini talep edebilir.

**Kaynak:** Privacy Notice giriş bölümü · CLOUD Act (2018)

---

### 5. Geri Bildiriminiz Üzerindeki Hakları Devrediyorsunuz

Terms and Conditions'a göre OffSec, kullandığınız ürünler
hakkında verdiğiniz her türlü geri bildirimi serbestçe ve
size herhangi bir tazminat ödemeksizin kullanabilir.
Bu geri bildirimlerden oluşturduğu türev çalışmaların tüm
fikri mülkiyet hakları OffSec'e aittir.

**Kaynak:** Terms and Conditions "Feedback" maddesi

---

### 6. Sınav Materyali Paylaşırsanız IP Haklarınızı Kaybedersiniz

Sınav raporları, lab raporları, walkthrough'lar ve sınava
yardımcı olabilecek diğer materyalleri şartları ihlal
ederek paylaşmanız halinde, paylaşım tarihinde bu
materyaller üzerindeki tüm fikri mülkiyet haklarınız
**otomatik olarak OffSec'e devredilmiş** sayılır.

**Kaynak:** Terms and Conditions "Exam Related Materials" maddesi

---

### 7. Sınav Davranış Verisi ve AI Eğitimi: Belgelenmiş Belirsizlik

Terms and Conditions'a göre platform, ürün kullanımına
ilişkin verileri ve kullanıcı geri bildirimlerini serbestçe
kullanabilir. Sınav sırasında alınan webcam ve ekran
kayıtlarının, problem çözme stratejilerinin ve komut
örüntülerinin AI model eğitiminde kullanılıp
kullanılamayacağı ToS'ta açıkça düzenlenmemiştir.

**Bağlam:** 2026 Mart ayında benzer platform TryHackMe,
"7 yıllık kullanıcı yolculuklarından" eğitilen NoScope
adlı AI pentesting aracını piyasaya sürdü. Platform
öncesinde kullanıcı verilerinin AI eğitiminde kullanıldığını
reddetmişti. Bu durum siber güvenlik topluluğunda büyük
tartışmaya yol açtı.

OffSec'in aynı uygulamayı benimsediğine dair kamuoyuyla
paylaşılmış belgesel bir kanıt şu an bulunmamaktadır.
Ancak mevcut ToS bu konuda açık bir güvence de
sağlamamaktadır.

**Kaynak:** Terms and Conditions "Feedback" ve "Data Privacy"
maddeleri · TryHackMe/NoScope tartışması (Mart 2026, kamuya açık)

---

## 🟡 Sarı Bayraklar

### Kamu Kaynaklarında Araştırma Yapılabilir

Privacy Notice'a göre OffSec, Academic Policy veya Terms
ihlali şüphesi durumunda "kamu alanı araştırması"
yapabilmektedir. Bu kamuya açık sosyal medya hesaplarınız,
blog yazılarınız ve forum paylaşımlarınızın incelenmesini
kapsamaktadır.

**Kaynak:** Privacy Notice "Investigations" bölümü

---

### Şartlar Değişebilir

OffSec şartları istediği zaman güncelleyebilir. Kullanmaya
devam etmek yeni şartları kabul anlamına gelir.

---

### Üçüncü Taraf Akreditasyon Aktarımı

Sertifikalarınızın üçüncü taraf kuruluşlar tarafından
akredite edilmesi durumunda kişisel verileriniz bu
kuruluşlara aktarılabilir. Hangi kuruluşların bu kapsama
girdiği belirtilmemiştir.

**Kaynak:** Privacy Notice "Third party accreditation" bölümü

---

### Google Analytics ile Davranışsal İzleme

Platform, demografik veriler ve ilgi alanı raporlaması
dahil Google Analytics kullanmaktadır. Ziyaretçi
davranışları, yaş ve cinsiyet gibi demografik bilgiler
Google altyapısında işlenmektedir.

**Kaynak:** OffSec Cookie Policy

---

## 🔵 Yapısal Değerlendirme

### ABD Şirketi ve Yetkili Hukuk

OffSec Services LLC New York'ta kayıtlı bir ABD şirketidir.
Uyuşmazlıklarda New York eyalet hukuku geçerlidir. Türk
kullanıcıların bireysel hukuki başvuru yolu coğrafi ve
mali açıdan son derece güçtür.

---

## KVKK Değerlendirmesi

| Kriter | Durum |
|---|---|
| KVKK'ya açık atıf | 🔴 Yok |
| Türkçe belge | 🔴 Yok |
| GDPR referansı | 🟢 Var |
| Veri silme hakkı | 🟢 Belgelenmiş |
| Veri saklama süresi | 🔴 Açık değil |
| Yetkili makam iletişimi | 🟡 İngilizce, e-posta ile |

---

## Dürüst Değerlendirme

OffSec, teknik güvenlik eğitimi alanında ciddi ve saygın
bir kuruluştur. "OffSec güvenilmez" şeklinde bir sonuç
bu analizden çıkarılamaz.

Ancak bu analiz şunu net olarak göstermektedir:

Siber güvenlik alanında çalışan profesyoneller bile
kullandıkları platformların şartlarını tam olarak okumadan
kabul etmektedir. Sınav proctoring kayıtları, işveren veri
erişimi, otomatik IP devri ve kamuya açık sertifika kaydı
gibi maddeler bu alanda çalışan herkesin bilmesi gereken
yapısal unsurlardır.

Özellikle Türkiye'de savunma, kamu kurumları veya kritik
altyapı alanlarında çalışan siber güvenlik uzmanları için
bu platformun kamuya açık kimlik kaydı ve ABD hukuku
yetki alanı ciddi bir OPSEC değerlendirmesi gerektirmektedir.

---

## Kaynaklar

| Belge | URL | Erişim Tarihi |
|---|---|---|
| Terms and Conditions | https://offsec.com/legal-docs/ | 24.04.2026 |
| Privacy Notice | https://www.offsec.com/legal/privacy-policy/ | 24.04.2026 |
| Cookie Policy | https://offsec.com/cookie-policy/ | 24.04.2026 |
| TryHackMe/NoScope tartışması | Kamuya açık — LinkedIn, Medium (Mart 2026) | 24.04.2026 |
| Wikipedia — OffSec | https://en.wikipedia.org/wiki/Offensive_Security | 24.04.2026 |
