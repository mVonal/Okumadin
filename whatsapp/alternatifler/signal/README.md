# Signal

**Geliştirici:** Signal Messenger LLC
**Üst kuruluş:** Signal Technology Foundation (501c3 kâr amacı gütmeyen vakıf)
**Merkez:** Mountain View, California, ABD
**Platform:** Android, iOS, Windows, macOS, Linux
**Açık kaynak:** Evet — github.com/signalapp (AGPL-3.0)
**Belge tarihi:** Gizlilik Politikası: 25 Mayıs 2018 (yürürlükte)
**Kaynak:** https://signal.org/legal/

> Bu analiz yalnızca bilgilendirme amaçlıdır, hukuki tavsiye niteliği
> taşımaz. Tüm tespitler Signal'in kendi yayımladığı belgeler esas
> alınarak hazırlanmıştır.

---

## Özet

Signal, güvenlik araştırmacıları ve gizlilik savunucuları tarafından
mesajlaşma uygulamaları arasında referans olarak gösterilen
platformdur. Temel argümanı şudur: toplamadığı veriyi paylaşması
mümkün değildir. Ancak bu itibar kısmen güvenlik camiasının
genel eğilimini yansıtmaktadır. Aşağıda hem güçlü yönler hem de
gerçek bilinmezlikler dürüstçe aktarılmaktadır.

---

## Skorlar

| Kriter | Değer |
|---|---|
| Genel risk skoru | 🟡 3 / 10 |
| Metadata toplama | 🟢 Minimal |
| Şeffaflık | 🟢 Açık kaynak, denetlenebilir |
| Ticari motivasyon | 🟢 Kâr amacı gütmeyen vakıf |
| Sunucu egemenliği | 🟡 ABD (ama veri minimal) |
| Belge güncelliği | 🔴 2018'den bu yana güncellenmemiş |

---

## Güçlü Yönler

### Kesin Veri Satmama Taahhüdü

Signal'in kendi Hizmet Şartlarında şu ifade yer almaktadır:
"Signal does not sell, rent or monetize your personal data
or content in any way — ever."

Bu ifade bir pazarlama sloganı değil, hizmet şartlarına
yazılmış bağlayıcı bir taahhüttür.

**Kaynak:** Signal Hizmet Şartları "Privacy of user data" maddesi

---

### Toplanan Veri Son Derece Sınırlı

Signal'in Gizlilik Politikasına göre platformun elinde
bulunan tek kişisel veri **telefon numaranızdır.** Bunun
yanı sıra teknik işleyiş için gerekli rastgele üretilmiş
kimlik doğrulama token'ları saklanmaktadır.

Mesaj içerikleri, grup üyelikleri, profil bilgileri ve
iletişim örüntüleri uçtan uca şifreli olduğundan
Signal sunucuları bunlara **erişememektedir.**

Bu taahhüdün gerçek dünyada sınanmış bir kanıtı mevcuttur:
2016 yılında ABD Federal Soruşturma Bürosu (FBI) bir mahkeme
kararıyla Signal'den kullanıcı verisi talep etmiştir. Signal'in
verebileceği yalnızca iki bilgi olmuştur: hesabın oluşturulduğu
tarih aralığı ve sunucuya son bağlantı tarihi. Bu süreç kamuya
açık mahkeme belgeleriyle kayıt altındadır.

**Kaynak:** Signal Gizlilik Politikası "Account Information"
ve "Messages" bölümleri · FBI mahkeme belgesi (2016, kamuya açık)

---

### Rehber Gizliliği Kriptografik Olarak Korunuyor

Gizlilik Politikasına göre rehber kişilerinin Signal kullanıcısı
olup olmadığını tespit etmek için telefon numaraları
**kriptografik hash** yöntemiyle işlenmektedir. Signal
sunucuları gerçek numaraları görmez; yalnızca hash
değerlerini karşılaştırır.

**Kaynak:** Signal Gizlilik Politikası "Contacts" bölümü

---

### Açık Kaynak ve Bağımsız Denetim

Signal'in tüm istemci ve sunucu kodu AGPL-3.0 lisansı altında
kamuya açıktır. Bağımsız güvenlik araştırmacıları kodu her an
denetleyebilmektedir.

**Kaynak:** github.com/signalapp

---

### Kâr Amacı Gütmeyen Yapı

Signal Technology Foundation, ABD'de 501(c)(3) statüsünde
tescilli bir kâr amacı gütmeyen vakıftır. Geliri bağışlardan
oluşmakta olup reklam geliri modeli bulunmamaktadır.

---

## 🟡 Dikkat Edilmesi Gereken Maddeler

### ABD Merkezli Kuruluş ve Mahkeme Yeri

Signal Messenger LLC, Mountain View, California'da kayıtlı bir
ABD şirketidir. Hizmet Şartlarının "Resolving Disputes" maddesine
göre tüm uyuşmazlıklar münhasıran **Kuzey Kaliforniya
mahkemelerinde, Kaliforniya hukukuna göre** çözülür.

Bu madde yapı olarak WhatsApp ile aynıdır. Farkı şudur: Signal'in
elinde paylaşabileceği anlamlı kullanıcı verisi son derece sınırlıdır.

**Kaynak:** Signal Hizmet Şartları "Resolving disputes" maddesi

---

### Tazminat Tavanı 100 USD

"Limitation of Liability" maddesine göre Signal'in azami
sorumluluğu **100 USD** ile sınırlandırılmıştır.

**Kaynak:** Signal Hizmet Şartları "Limitation of liability"

---

### Gizlilik Politikası 2018'den Bu Yana Güncellenmemiş

Signal'in mevcut Gizlilik Politikası 25 Mayıs 2018 tarihlidir.
Yedi yıldır resmi olarak güncellenmemiş olması şeffaflık
açısından önemli bir eksikliktir.

**Kaynak:** Signal Gizlilik Politikası "Updated" notu

---

### Telefon Numarası Zorunlu

Hesap açmak için telefon numarası zorunludur. Mart 2024 itibarıyla
kullanıcı adı özelliği eklenmiş olup artık numaranızı diğer
kullanıcılardan gizleyebilirsiniz. Ancak kayıt için zorunluluk devam
etmektedir.

---

## ⚠️ Dürüst Değerlendirme: Signal Hakkında Bilinmezler

Signal güvenlik camiasında neredeyse tartışmasız referans olarak
sunulur. Bu eğilim meşru temellere dayanmakla birlikte bazı
önemli bilinmezlikleri göz ardı etmek analiz taraflılığı yaratır.

**"Kodu açık, ama çalıştırdıkları kodu denetleyemezsiniz"**

Açık kaynak kod yayımlanmış olması, Signal'in sunucularında
gerçekte ne çalıştığını doğrulamayı mümkün kılmaz. Kapalı bir
veri merkezinde hangi kodun aktif olduğunu bağımsız olarak
doğrulamak teknik olarak imkânsızdır. Açık kaynak bir güven
göstergesidir, mutlak bir kanıt değildir.

**CLOUD Act riski gerçektir**

Signal "toplamadığı veriyi veremez" argümanıyla güçlüdür. Ancak
ABD şirketi olması nedeniyle CLOUD Act kapsamında yasal taleplere
muhatap olabilir. Bugün minimal veri topladığı doğru olsa bile
politika değişiklikleri her zaman mümkündür.

**Merkezi yapı ve erişim engeli riski**

Signal'in mimarisi merkezi sunuculara dayanmaktadır. Bu durum
tek nokta kırılganlığı yaratır. Nitekim Rusya, İran, Çin ve
Venezuela Signal'i erişim engeliyle karşılamıştır. Matrix/NEXT
gibi federatif yapılar bu riski dağıtır.

**Sürdürülebilirlik belirsizliği**

Tamamen bağışlarla finanse edilmektedir. Finansal baskı altında
iş modelinin değişip değişmeyeceği bilinmemektedir.

**Sonuç:** Signal bugün itibarıyla teknik güvenlik açısından
güçlü seçeneklerden biridir. Ancak "altın standart"
nitelendirmesi kısmen güvenlik camiasının genel eğilimini
yansıtmaktadır. Her kullanıcının kendi tehdit modeline göre
değerlendirmesi önerilir.

---

## Kimler İçin Uygundur?

- Maksimum gizlilik ve güvenlik arayanlar
- Gazeteciler, avukatlar, aktivistler
- Açık kaynak denetimi öncelik olarak görenler

## Kimler İçin Sınırlı Kalabilir?

- Verilerinin Türkiye'de kalmasını kesin olarak isteyenler
- Türkçe yasal belge arayanlar
- Erişim engeli riskine karşı dayanıklılık isteyenler
- Federatif/kendi sunucu yapısı arayanlar

---

## Kaynaklar

| Belge | URL | Erişim Tarihi |
|---|---|---|
| Hizmet Şartları ve Gizlilik Politikası | https://signal.org/legal/ | 23.04.2026 |
| Kaynak Kodu | https://github.com/signalapp | 23.04.2026 |
| GDPR Desteği | https://support.signal.org/hc/en-us/articles/360007059412 | 23.04.2026 |
