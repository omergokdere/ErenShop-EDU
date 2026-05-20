# ErenShop Eğitim Platformu

İş analisti yetkinliklerini ölçen iki modülden oluşur:

1. **Analiz Teknik Dokümanı Egzersizi** — rastgele bir geliştirme talebi alırsın, Word şablonunu doldurursun, sistem otomatik puanlar.
2. **Dinamik SQL Bilgi Testi** — havuzdan rastgele sorularla her seferinde farklı bir test.

Tek bir LLM/dış API kullanılmaz — değerlendirme tamamen lokal ve kural tabanlıdır.

---

## Kurulum

### 1. SQL betiklerini çalıştır (yalnız bir kez)

SSMS'te sırayla:

```sql
-- Yeni tablolar (TrainingUsers, BusinessRequests, RequestSubmissions,
-- SqlQuestions, SqlTests, SqlTestQuestions)
:r sql/08_training_tables.sql

-- 40 hazır geliştirme talebi
:r sql/09_seed_business_requests.sql

-- 60 SQL test sorusu (kolay/orta/zor)
:r sql/10_seed_sql_questions.sql
```

> SSMS'te ":r" yerine dosyaları açıp F5 ile de çalıştırabilirsin.

### 2. Python bağımlılıkları

```powershell
.\venv\Scripts\activate
pip install -r requirements.txt
```

Yeni eklenenler: `python-docx`, `python-multipart`.

### 3. API'yi başlat

```powershell
.\run.bat
```

Eğitim platformu: <http://localhost:8000/frontend/training.html>

---

## Kullanım — Eren

### Analiz Egzersizi

1. **Eğitim** sayfasından **Analiz Egzersizi** sekmesine git.
2. **🎲 Yeni Talep Al** → rastgele bir geliştirme talebi gelir.
3. **📥 Şablonu İndir** → kapak sayfasında talebin yazılı olduğu Word dosyası iner.
4. Word'ü doldur:
   - Bölüm başlıklarını **DEĞİŞTİRME** (sistem başlık metnine göre arama yapar).
   - Her bölümün altındaki italik gri yol gösterici metinleri silebilirsin.
   - Köşeli parantez içindeki örnekleri kendi içeriğinle değiştir.
   - Bir bölümün altındaki placeholder metnini olduğu gibi bırakırsan "boş" sayılır ve puanı düşer.
5. Dosyayı **Yükle ve Değerlendir** alanından gönder.
6. Sistem iki skor verir:
   - **Yapısal Skor**: bölüm başlıkları var mı, her bölüm yeterli uzunlukta mı?
   - **İçerik Skoru**: talebin beklediği anahtar kelimeler dokümanda geçiyor mu, toplam kelime sayısı yeterli mi?
7. **Toplam Puan** = yapısal + içerik / 2.

> Aynı talebi tekrar deneyebilirsin (puanını iyileştirmek için).
> Bir talep **onaylandığında** artık o talep sana tekrar gelmez.

### SQL Testi

1. **SQL Testi** sekmesinden test ayarla (kolay/orta/zor adetleri).
2. **🚀 Testi Başlat** → soru havuzundan rastgele sorular gelir.
3. Soru tipleri:
   - **Çoktan seçmeli** → radio butonla işaretle.
   - **Boşluk doldurma** → kısa cevap yaz (büyük/küçük harf duyarsız).
   - **SQL kod yaz** → kısa SQL ifadesi yaz (noktalı virgül, fazla boşluk önemsiz).
4. Cevap otomatik kaydedilir (yazı yazınca 600ms sonra kaydedilir).
5. **✅ Testi Tamamla** → toplam skor + soru bazlı doğru/yanlış + açıklamalar gösterilir.

> Her yeni test farklı sorularla gelir (rastgele NEWID() ile seçilir).

---

## Kullanım — Ömer (Admin)

1. Sağ üstten kullanıcı seçiminde **Omer (admin)**'i seç.
2. **Admin İnceleme** sekmesi açılır.
3. Bekleyen submission'ları görür, **✓ Onayla** veya **✗ Reddet** edersin.
4. Not bırakabilirsin (red sebebi açıklaması gibi).
5. Onaylanan talep Eren'e bir daha gelmez. Reddedilen talep tekrar denenebilir.

---

## Şablondaki Bölümler

Sektörde standart BRD/SRS hibrit yapısı:

1. Doküman Bilgileri (versiyon, hazırlayan, tarih)
2. Yönetici Özeti
3. Amaç ve Kapsam (kapsam DIŞI dahil!)
4. Mevcut Durum Analizi
5. Paydaşlar
6. Fonksiyonel Gereksinimler (FG-01, FG-02 ...)
7. Fonksiyonel Olmayan Gereksinimler
8. İş Kuralları (IK-01, IK-02 ...)
9. Süreç Akışı (Happy + alternatif)
10. Veri Modeli (yeni tablo / kolon, FK ilişkileri)
11. Kullanıcı Arayüzü / Mock-up
12. Entegrasyonlar
13. Kabul Kriterleri (KK-01, KK-02 ...)
14. Test Senaryoları (TS-01: ön koşul, adımlar, beklenen sonuç)
15. Riskler ve Varsayımlar
16. Açık Sorular

---

## Puanlama Detayı (Kural Tabanlı)

### Yapısal (50%)

Her bölüm için:

| Durum | Puan |
|---|---|
| Bölüm hiç yok | 0 |
| Yalnız placeholder duruyor | %20 |
| Çok kısa (< yarı min_words) | %50 |
| Kısa (< min_words, > yarı) | %75 |
| Yeterli (>= min_words) | %100 |

Zorunlu bölümler 2 puan, opsiyonel 1 puan ağırlığında.

### İçerik (50%)

- **Anahtar Kelime (%70)**: Talebin `ExpectedKeywords` listesindeki kelimelerin kaçı dokümanda geçiyor?
- **Toplam Kelime (%30)**: Talebin `MinTotalWords` değeri karşılanıyor mu?

---

## Geliştirici Notları

- `app/services/document_template.py` — Şablon bölümleri tek noktada (`TEMPLATE_SECTIONS`).
- `app/services/document_evaluator.py` — Saf kural tabanlı, deterministik. LLM yok.
- `app/services/training_service.py` — DB işlemleri ve iş mantığı.
- `app/routes/training_routes.py` — REST endpoint'leri.
- `frontend/training.{html,css,js}` — Tek sayfalık eğitim arayüzü.
- `uploads/` — Yüklenen Word dosyaları burada saklanır.

### Yeni Talep Ekleme

`sql/09_seed_business_requests.sql` dosyasına `INSERT INTO BusinessRequests ...` ekle, çalıştır.

### Yeni SQL Sorusu Ekleme

`sql/10_seed_sql_questions.sql` dosyasına ekle. Format:
- `multiple_choice`: `OptionsJson` = `N'["A","B","C","D"]'`, `CorrectAnswer` = `N'0..3'`
- `fill_in_blank`: `CorrectAnswer` = direkt metin
- `short_code`: `CorrectAnswer` = SQL kodu (normalize edilip karşılaştırılır)
