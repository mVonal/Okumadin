# OKM-RM v1.0
## Okumadın Risk Methodology

> Bu belge Okumadın projesinin çekirdek metodolojisidir ve
> koddan daha değerlidir. Kod yeniden yazılabilir; bu belge
> değişirse veri tabanının tamamı yeniden değerlendirilir.
> Bu nedenle metodoloji nadiren, dikkatle ve versiyonlanarak
> güncellenir.

**Versiyon:** 1.0
**Dondurulma tarihi:** [22.07.2026]
**Durum:** Yürürlükte

---

## 1. Metodolojinin Amacı ve Kapsamı

OKM-RM, dijital servislerin kullanıcı sözleşmelerini, gizlilik
politikalarını ve çerez politikalarını tutarlı, tekrarlanabilir
ve doğrulanabilir biçimde puanlayan standartlaştırılmış bir
değerlendirme sistemidir. Ürettiği puan **OKM Score** olarak
adlandırılır.

**OKM Score, hukuki uygunluğu değil; kullanıcı açısından
dijital güven riskini ölçer.**

Bu ayrım metodolojinin temelidir. Bir servis tüm yasal
yükümlülüklerini yerine getiriyor olsa bile, kullanıcı
açısından yüksek güven riski taşıyabilir. Tersi de mümkündür.
"KVKK cezası aldı diye neden yüksek puan?" veya "yasalara
uygun diye neden düşük değil?" sorularının cevabı her zaman
aynıdır: OKM, hukuki uygunluğu değil, kullanıcının verdiği
güven riskini ölçer.

OKM Score bir görüş değildir. Metodolojinin çıktısıdır.
"Neden bu puan?" sorusunun cevabı her zaman "metodoloji bunu
üretti" olmalıdır.

---

## 2. Metodolojinin Ölçmedikleri (Limitations)

OKM'nin neyi ölçtüğü kadar neyi ölçmediği de metodolojinin
parçasıdır. OKM **yalnızca** yayınlanan resmi belgelerin
kullanıcı açısından oluşturduğu riski puanlar.

OKM şunları ölçmez:
- Servisin belgelerinde yazanı gerçekten yapıp yapmadığını
- Veri sızıntısı veya ihlal ihtimalini
- Kod güvenliğini veya teknik açıkları
- Şirketin niyetini veya gelecekte ne yapacağını
- Uygulamanın teknik güvenlik düzeyini

OKM, bir davranış denetimi değil, bir belge değerlendirmesidir.
Bu sınır, kullanıcıya karar dayatmama ilkesinin metodolojik
karşılığıdır.

---

## 3. Her Bulgu Üç Katmana Ayrılır

OKM-RM'nin temel ilkesi: olgu, yorum ve risk birbirine
karıştırılmaz. Her bulgu üç katmanda ifade edilir.

**FACT (Olgu)** — Belgede birebir ne yazıyor? Doğrudan
alıntı veya sadık aktarım. Yoruma yer yok.

**INTERPRETATION (Yorum)** — Bu olgu ne anlama geliyor?
Teknik veya hukuki çıkarım.

**RISK (Risk)** — Bu durum kullanıcı için neden önemli?

Bu ayrım hukuki koruma sağlar: FACT saldırılamaz çünkü
şirketin kendi belgesidir. INTERPRETATION ve RISK açıkça
yorum olarak etiketlendiği için ifade özgürlüğü kapsamındadır.

---

## 4. Kanıt Seviyeleri (Evidence Levels)

Her FACT bir kanıt koduyla etiketlenir. Kodlar kaynak tipine
değil, **kanıt gücüne** göre tanımlanmıştır; böylece metodoloji
her ülkenin düzenleyici çerçevesine (KVKK, GDPR, FTC, ICO,
EDPB, CNIL vb.) uyum sağlar.

| Kod | Tanım | Örnek |
|---|---|---|
| A | Birincil resmi kaynak | Şirketin kendi sözleşmesi/politikası |
| B | Resmi kurum / düzenleyici | KVKK, GDPR otoritesi, mahkeme kararı |
| C | Teknik doğrulanabilir kanıt | Trafik analizi, kod incelemesi |
| D | Güvenilir üçüncü taraf | Akademik yayın, güvenlik raporu |
| E | Editoryal yorum / uzman çıkarımı | Metodolojik değerlendirme |

Kural: D ve E seviyesi bulgular, yorum olduğu açıkça
belirtilmeden RISK katmanına taşınamaz. A ve B doğrudan
olgu olarak sunulabilir.

---

## 5. Bulgu Sınıflandırması (Taxonomy)

Her bulgu, standart bir kategori etiketi taşır. Bu etiketler
JSON şemasının ve gelecekteki API sorgularının temelidir.

| Etiket | Kapsam |
|---|---|
| DATA_TRANSFER | Yurt dışı veya üçüncü ülke veri aktarımı |
| METADATA | Metadata toplama (kim, ne zaman, ne sıklıkla) |
| CONSENT | Rıza mekanizmaları |
| COOKIES | Çerez ve izleyici kullanımı |
| RETENTION | Veri saklama süreleri |
| THIRD_PARTY | Üçüncü taraf paylaşımı |
| GOVERNING_LAW | Geçerli hukuk |
| JURISDICTION | Yetkili mahkeme |
| AI_USAGE | Yapay zeka ile veri işleme |
| CHILDREN | Çocuk verileri |
| PROFILING | Profilleme ve hedefleme |
| ACCOUNT_DELETION | Hesap ve veri silme |
| BUSINESS_MESSAGES | İşletme iletişimi |
| CLOUD_BACKUP | Bulut yedekleme |
| LAW_ENFORCEMENT | Kolluk / devlet talepleri |

Bu liste versiyonla genişletilebilir; mevcut etiketler
değiştirilemez.

---

## 6. OKM Score Nasıl Hesaplanır?

OKM Score, altı kriterin ağırlıklı ortalamasıdır.

| Kriter | Ağırlık |
|---|---|
| Yurt dışı veri aktarımı | %20 |
| Üçüncü taraf paylaşımı | %15 |
| Metadata ve veri toplama kapsamı | %15 |
| KVKK / veri koruma uyumu | %20 |
| Belge şeffaflığı ve erişilebilirliği | %15 |
| Yetkili hukuk ve mahkeme | %15 |

Her kriter 1-10 arası puanlanır (puanlama rehberi Ek A'da).
Ağırlıklı ortalama alınır, 10 üzerinden OKM Score elde edilir.

---

## 7. Görsel Dil — OKM Score Skalası

Görsel dil metodolojinin parçasıdır. İnsanlar renklere
sayılardan daha güçlü tepki verir.

| OKM Score | Kategori | Renk |
|---|---|---|
| 1.0 – 2.9 | Low | 🟢 |
| 3.0 – 4.9 | Moderate | 🟡 |
| 5.0 – 6.9 | Elevated | 🟠 |
| 7.0 – 8.4 | High | 🔴 |
| 8.5 – 10 | Critical | ⚫ |

Kritik (⚫) kategori, istisnai riskleri sıradan yüksek
riskten ayırmak için ayrılmıştır.

---

## 8. Confidence Score (Güven Düzeyi)

Her OKM Score'un yanında bir **Confidence Score** bulunur.
Bu, "bu puanı verirken ne kadar eminiz?" sorusunu ölçer.

Aynı OKM Score, farklı şeffaflık düzeyindeki iki şirkette
aynı güvenilirliğe sahip değildir. Her şeyi açıkça belgeleyen
bir şirketle hiçbir şey belirtmeyen bir şirket aynı puanı
alabilir; ancak bizim o puana olan güvenimiz farklıdır.

Confidence Score şunlara göre belirlenir: belgelerin
erişilebilirliği, açıklık düzeyi, kanıt seviyelerinin
dağılımı (A-B ağırlıklı ise yüksek, D-E ağırlıklı ise düşük).

**Not:** Confidence Score alanı v1.0'da tanımlanmıştır.
Hesaplama formülü v1.1'de belirlenecektir. v1.0 analizlerinde
bu alan "hesaplanmadı" olarak işaretlenir.

---

## 9. Versiyonlama

Küçük düzeltmeler (yazım, örnek): v1.0 → v1.1.
Ağırlık veya kriter değişikliği: v1.0 → v2.0.
Ana versiyon değişikliğinde tüm mevcut analizler yeniden
puanlanır ve her analizin change log'una işlenir.

---

## 10. Değişmezler

Versiyon değişse bile korunan ilkeler:

- OKM Score bir görüş değil, metodoloji çıktısıdır
- OKM hukuki uygunluğu değil, dijital güven riskini ölçer
- Kanıtlanamayan hiçbir iddia yayımlanmaz
- Olgu, yorum ve risk her zaman ayrı tutulur
- AI taslak üretebilir ama asla yayına karar veremez
- Analizler zamanla değişebilir; bu bir kusur değil, özelliktir
- Hatalar saklanmaz; change log'da kalır

---

## Ek A — Kriter Puanlama Rehberi

**Yurt dışı veri aktarımı**
1-2: Veri yurt içinde, uyumlu aktarım mekanizması
4-6: Belirsiz veya standart sözleşmeyle güvencelenmiş
8-10: Yabancı sunucu, ihlal kayıtlı

**Üçüncü taraf paylaşımı**
1-2: Paylaşım yok veya zorunlu teknik altyapı
4-6: Sınırlı, açık rızaya dayalı
8-10: Reklam ekosistemiyle kapsamlı paylaşım

**Metadata ve veri toplama kapsamı**
1-2: Yalnızca hizmet için zorunlu minimum
4-6: Orta düzey kullanım ve davranış verisi
8-10: Konum, cihaz, zamanlama, kimlik, finansal veri

**KVKK / veri koruma uyumu**
1-2: Açık atıf, aydınlatma mevcut, ihlal yok
4-6: Kısmi uyum, eksiklikler mevcut
8-10: İhlal kayıtlı veya düzenlemeye hiç atıf yok

**Belge şeffaflığı ve erişilebilirliği**
1-2: Yerel dilde, kamuya açık URL, güncel
4-6: Yabancı dilde veya kısmen erişilebilir
8-10: Kamuya açık URL yok, belge eksik veya kırık link

**Yetkili hukuk ve mahkeme**
1-2: Yerel hukuk, yerel mahkemeler
4-6: Belirsiz veya karma yetki
8-10: Yabancı hukuk, bireysel başvuru imkânsız
