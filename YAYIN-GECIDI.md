# Yayın Geçidi — Definition of Done

> Hiçbir analiz bu geçitten geçmeden yayınlanamaz.
> Bu kontrol, kalitenin kişinin o günkü dikkatine değil,
> sisteme bağlı olmasını sağlar.
> Anayasa Madde 3'ün ("kanıtlanamayan iddia yayımlanmaz")
> operasyonel karşılığıdır.

Bir analizin durumu, tüm kutular işaretlenene kadar
"published" olamaz. Kontrolü yapan kişi, aşağıya adını
ve tarihi yazar.

---

## Katman 1 — İçerik Doğruluğu

Her iddianın belgede gerçekten geçtiğini garanti eder.

- [ ] Her bulgu FACT / INTERPRETATION / RISK olarak ayrılmış
- [ ] Her FACT'in metni, kaynak belgede birebir doğrulandı
      (kaynak açıldı, ifade orada gerçekten var)
- [ ] Her FACT'in kaynak konumu doğru: bölüm, madde veya
      paragraf belgeyle eşleşiyor
- [ ] Hiçbir INTERPRETATION veya RISK, FACT gibi sunulmamış
- [ ] D veya E kanıt seviyeli hiçbir bulgu, olgu gibi
      yayımlanmamış — açıkça yorum olarak etiketlenmiş

## Katman 2 — Yapısal Bütünlük

Makinenin veriyi okuyabilmesini garanti eder.

- [ ] Her FACT bir kanıt kodu (A-E) taşıyor
- [ ] Her bulgu bir taxonomy etiketi taşıyor
- [ ] Her bulgu bir severity kodu (code + display) taşıyor
- [ ] JSON şeması eksiksiz dolduruldu (bulgu + analiz)
- [ ] Tüm kaynaklar URL ve erişim tarihiyle kayıtlı
- [ ] Belge hash'leri (sha256) kaydedildi
- [ ] OKM Score, kriter puanlarından doğru hesaplandı

## Katman 3 — Kültürel Uyum

Anayasa'ya uygunluğu garanti eder.

- [ ] Hiçbir yerde kullanıcıya karar dayatılmıyor
      ("sil", "kullanma" değil; "şu riski içeriyor")
- [ ] Metin, belirli bir şirkete yönelik itham içermiyor;
      yalnızca şirketin kendi belgesine dayanıyor
- [ ] "X satıyor/yapıyor" değil, "X'in belgesine göre Y
      mümkün" dili kullanılmış
- [ ] Analiz, üretim izini taşıyor (AI taslak / insan editör)

---

## Onay

Yukarıdaki tüm kutular işaretlendi.

- **İnceleyen:** _______________
- **Tarih:** _______________
- **Analiz durumu → "published" olarak güncellendi:** [ ]

---

## Geçit Başarısız Olursa

Herhangi bir kutu işaretlenemiyorsa, analiz "published"
olamaz. Durum "review" veya "draft" olarak kalır.
Eksik giderilir, geçit baştan uygulanır.

Anayasa Madde 2 gereği: geç yayınlamak, yanlış yayınlamaktan
her zaman iyidir.
