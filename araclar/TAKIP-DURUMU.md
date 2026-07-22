# ToS Takip Sistemi — Kapsam Durumu

**Bot sürümü:** v2.1
**Son güncelleme:** 22.07.2026

## Otomatik takip edilenler

| Platform | Belge | Durum |
|---|---|---|
| WhatsApp | Hizmet Şartları | ✅ |
| WhatsApp | Gizlilik Politikası | ✅ |
| WhatsApp | Çerez Politikası | ✅ |
| BiP | Kullanım Koşulları | ✅ |
| Signal | Hizmet Şartları ve Gizlilik | ✅ |
| OffSec | Terms and Conditions | ✅ |
| OffSec | Privacy Notice | ✅ |

## Takip edilemeyenler — manuel kontrol gerekiyor

| Platform | Belge | Sebep |
|---|---|---|
| BiP | Aydınlatma Metni | JavaScript ile yükleniyor |
| Trendyol | Üyelik Sözleşmesi | JavaScript ile yükleniyor |
| Trendyol | Aydınlatma Metni | JavaScript ile yükleniyor |
| Trendyol | Çerez Politikası | JavaScript ile yükleniyor |

Bu belgeler ayda bir manuel kontrol edilir.
Kalıcı çözüm: Playwright entegrasyonu (Faz 1 görevi).

## Bilinen sınırlar

- Bot yalnızca metin değişikliğini tespit eder; değişikliğin
  analizi etkileyip etkilemediğine insan karar verir (Anayasa m.7)
- 40 karakterden kısa değişiklikler gürültü sayılır ve raporlanmaz
- Dinamik içerik çift çekim kesişimiyle elenir
