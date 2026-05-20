# 🎓 ErenShop EDU

> **İş Analisti & Backend Geliştirici Eğitim Platformu**
> Hazırlayan: **Ömer Gökdere** — kardeşi Eren Sarıteke'nin iş analisti olarak yetişmesi için geliştirilmiştir.

ErenShop EDU, gerçek bir e-ticaret API'si üzerine inşa edilmiş, çok modüllü bir öğrenme ortamıdır. Hem **iş analizi** hem **backend geliştirme** (FastAPI), **SQL** ve **API testi** (Postman / Swagger) becerilerini ölçülebilir egzersizlerle kazandırmayı hedefler.

---

## 📚 İçindekiler

- [Genel Bakış](#-genel-bakış)
- [Neler Yapılabilir?](#-neler-yapılabilir)
- [Mimari](#-mimari)
- [Kurulum](#-kurulum)
- [Çalıştırma](#-çalıştırma)
- [Erişim Adresleri](#-erişim-adresleri)
- [Klasör Yapısı](#-klasör-yapısı)
- [Eğitim Modülleri](#-eğitim-modülleri-detay)
- [Teknolojiler](#-teknolojiler)
- [Lisans & İletişim](#-lisans--iletişim)

---

## 🌟 Genel Bakış

Proje üç bileşenden oluşur:

| Bileşen | Açıklama |
|---|---|
| 🛒 **Mağaza (ErenShop)** | Vanilla JS + FastAPI ile yazılmış mini e-ticaret uygulaması. Kategoriler, ürünler, müşteri, sepet, sipariş, ödeme, raporlar. |
| 📖 **Dokümanlar** | Tek sayfada toplanmış kapsamlı eğitim materyali: kurulum, API dokümanı, 5 günlük eğitim akışı, SQL ve Postman notları. |
| 🎓 **Eğitim Platformu** | Eren'in iş analisti gibi düşünmesini ölçen iki egzersiz modülü (analiz dokümanı + SQL bilgi testi). |

Hiçbir dış LLM/AI servisi kullanılmaz — değerlendirme **tamamen lokal ve kural tabanlıdır**.

---

## 🎯 Neler Yapılabilir?

### 📝 Modül 1 — Analiz Teknik Dokümanı Egzersizi

**Senaryo:** Eren'e rastgele bir geliştirme talebi atanır (örn. "Kupon Kodu Sistemi", "Sadakat Puanı", "B2B Müşteri Tipi"). Eren bir iş analisti gibi Word dokümanı doldurur, sistem otomatik puanlar, Ömer son onayı verir.

- ✅ **40 hazır geliştirme talebi** (kolay/orta/zor karışım — kupon, sadakat, abonelik, B2B, çoklu depo, A/B test, vb.)
- ✅ **Sektör standardı şablon**: BRD/SRS hibrit yapısında 16 bölüm (Yönetici Özeti, Amaç/Kapsam, Fonksiyonel Gereksinimler, İş Kuralları, Süreç Akışı, Veri Modeli, Kabul Kriterleri, Test Senaryoları, vb.)
- ✅ **Kural tabanlı puanlama**: yapısal skor (başlık varlığı, min kelime sayısı, placeholder kontrolü) + içerik skoru (beklenen keyword'ler, toplam kelime sayısı)
- ✅ **Referans örnek doküman**: tam doldurulmuş "Favori Ürünler Listesi" analizini referans olarak indirebilir
- ✅ **Admin onay akışı**: Ömer bekleyenleri görür, onaylar/reddeder, not bırakır

### 💾 Modül 2 — Dinamik SQL Bilgi Testi

**Senaryo:** Eren'in SQL bilgisini ölçen, her başlatıldığında **farklı sorulardan** oluşan test.

- ✅ **60 SQL sorusu** (20 kolay + 25 orta + 15 zor)
- ✅ **3 soru tipi**: çoktan seçmeli (radio), boşluk doldurma, kısa SQL kod yazma
- ✅ **Konu kapsamı**: SELECT/WHERE/ORDER BY, INSERT/UPDATE/DELETE, JOIN, GROUP BY/HAVING, aggregate, subquery, CASE WHEN, window function (ROW_NUMBER + PARTITION), CTE, transaction
- ✅ **Otomatik puanlama**: cevap → string eşleşme (normalize: küçük harf, boşluk, noktalı virgül göz ardı)
- ✅ **Sonuç ekranı**: her soru için doğru/yanlış, doğru cevap, açıklama
- ✅ **Geçmiş takibi**: tüm tamamlanan testler ve skorları görüntülenir

### 🛒 Modül 3 — Mağaza & API Testi

ErenShop API mağazası, Swagger ve Postman üzerinden test edilebilir. **5 günlük yapılandırılmış eğitim akışı** mevcut:

1. **Gün 1 — SQL & Veritabanı**: SSMS, tablo oluşturma, PK/FK, temel sorgular
2. **Gün 2 — API Çalıştırma**: FastAPI, Swagger, Postman, GET endpoint'leri
3. **Gün 3 — POST/PUT/DELETE**: Yeni kayıt, güncelleme, soft delete, HTTP status kodları
4. **Gün 4 — Sepet, Sipariş, Transaction**: ACID, stok düşme, ödeme simülasyonu, hata senaryoları
5. **Gün 5 — Raporlar & JOIN**: GROUP BY, çoklu JOIN, raporlama endpoint'leri

---

## 🏗️ Mimari

```
┌─────────────────────────────────────────────────────┐
│                  Frontend (Vanilla JS)               │
│  Mağaza • Eğitim Platformu • Dokümanlar             │
└───────────────────┬─────────────────────────────────┘
                    │ HTTP (fetch)
                    ▼
┌─────────────────────────────────────────────────────┐
│              FastAPI Backend (Python)                │
│  ┌─────────────┬─────────────┬──────────────────┐  │
│  │   Routes    │  Services   │   Schemas        │  │
│  │ (HTTP layer)│ (business)  │ (Pydantic)       │  │
│  └─────────────┴─────────────┴──────────────────┘  │
│  • Categories • Products • Customers • Cart         │
│  • Orders • Payments • Reports • Training (NEW)     │
└───────────────────┬─────────────────────────────────┘
                    │ pyodbc
                    ▼
┌─────────────────────────────────────────────────────┐
│         Microsoft SQL Server (ErenShopDB)            │
│  Mağaza Tabloları: 8 tablo + Training Tabloları: 6  │
└─────────────────────────────────────────────────────┘
```

**Tasarım prensipleri:**
- Mağaza ve eğitim modülleri **aynı API**'nin parçası — tek FastAPI uygulaması
- **Hiç LLM yok** — tüm değerlendirme deterministik kural tabanlı
- **Single Source of Truth**: doküman şablon bölüm tanımları hem üretim hem değerlendirme için tek dosyada (`document_template.py`)
- **Standart response formatı**: `{ success, message, data }` — tüm endpoint'lerde tutarlı

---

## ⚙️ Kurulum

### Ön Koşullar

| Yazılım | Sürüm | Notlar |
|---|---|---|
| Python | 3.10+ | `Add to PATH` işaretli kur |
| Microsoft SQL Server | 2019/2022 | Express edition yeterli |
| SQL Server Management Studio (SSMS) | 19+ | DB yönetimi için |
| ODBC Driver for SQL Server | 17+ | pyodbc bağlantısı için zorunlu |
| Postman (opsiyonel) | Güncel | API test için |
| Git | Güncel | Kod indirmek için |

### Adım 1 — Repoyu Klonla

```powershell
git clone https://github.com/omergokdere/ErenShop-EDU.git
cd ErenShop-EDU
```

### Adım 2 — Sanal Ortam Kur

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Adım 3 — Ortam Değişkenleri

```powershell
copy .env.example .env
```

`.env` dosyasını aç ve gerekirse düzenle (varsayılan ayarlar Windows Authentication ile çalışır):

```env
DB_SERVER=localhost
DB_NAME=ErenShopDB
DB_USER=               # SQL Auth kullanıyorsan doldur
DB_PASSWORD=           # SQL Auth kullanıyorsan doldur
DB_DRIVER=ODBC Driver 17 for SQL Server
```

### Adım 4 — Veritabanını Kur

SSMS'te ErenShopDB'ye bağlandıktan sonra sırayla F5 ile çalıştır:

**Mağaza tabloları:**
```
sql/01_create_database.sql
sql/02_create_tables.sql      → 8 tablo (Categories, Products, Customers, Cart, Orders, ...)
sql/03_seed_data.sql          → Örnek mağaza verileri
```

**Eğitim platformu tabloları:**
```
sql/08_training_tables.sql              → 6 tablo (TrainingUsers, BusinessRequests, ...)
sql/09_seed_business_requests.sql       → 40 geliştirme talebi
sql/10_seed_sql_questions.sql           → 60 SQL test sorusu
```

> ⚠️ Sıralama önemli — bir sonraki script önceki tabloları kullanır.

---

## ▶️ Çalıştırma

```powershell
.\run.bat
```

veya:

```powershell
uvicorn app.main:app --reload --port 8000
```

Sunucu başladığında:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

---

## 🔗 Erişim Adresleri

| Adres | Açıklama |
|---|---|
| <http://localhost:8000/frontend/index.html> | 🛒 **Mağaza** — ürün listele, sepete ekle, sipariş ver |
| <http://localhost:8000/frontend/training.html> | 🎓 **Eğitim Platformu** — analiz egzersizi + SQL testi |
| <http://localhost:8000/frontend/docs.html> | 📖 **Dokümanlar** — kurulum, eğitim akışı, API, SQL/Postman notları |
| <http://localhost:8000/docs> | 📋 **Swagger UI** — tüm endpoint'leri etkileşimli test et |
| <http://localhost:8000/redoc> | 📄 **ReDoc** — alternatif API dokümanı |

---

## 📁 Klasör Yapısı

```
ErenShop-EDU/
├── app/
│   ├── main.py                       # FastAPI uygulaması
│   ├── config.py                     # Ortam ayarları
│   ├── database.py                   # pyodbc bağlantı yönetimi
│   ├── routes/                       # HTTP endpoint katmanı
│   │   ├── category_routes.py
│   │   ├── product_routes.py
│   │   ├── customer_routes.py
│   │   ├── cart_routes.py
│   │   ├── order_routes.py
│   │   ├── payment_routes.py
│   │   ├── report_routes.py
│   │   └── training_routes.py        # Eğitim modülü (16 endpoint)
│   ├── services/                     # İş mantığı + DB işlemleri
│   │   ├── ...
│   │   ├── training_service.py
│   │   ├── document_template.py      # Word şablon üreteci
│   │   └── document_evaluator.py     # Kural tabanlı değerlendirici
│   ├── schemas/                      # Pydantic veri modelleri
│   └── utils/                        # Yardımcı fonksiyonlar
├── sql/                              # Tüm SQL scriptleri
│   ├── 01_create_database.sql
│   ├── ...
│   ├── 08_training_tables.sql
│   ├── 09_seed_business_requests.sql
│   └── 10_seed_sql_questions.sql
├── frontend/                         # Vanilla JS arayüz
│   ├── index.html                    # Mağaza
│   ├── training.html                 # Eğitim platformu
│   ├── docs.html                     # Dokümanlar
│   ├── style.css / training.css
│   └── app.js / training.js
├── docs/                             # Markdown dokümantasyon
│   ├── API_DOKUMANI.md
│   ├── KURULUM.md
│   ├── EGITIM_AKISI.md
│   ├── EGITIM_PLATFORMU.md
│   ├── SQL_EGITIM_NOTLARI.md
│   └── POSTMAN_EGITIM_NOTLARI.md
├── postman/                          # Postman collection + environment
├── uploads/                          # Yüklenen Word dosyaları (gitignored)
├── requirements.txt
├── .env.example
├── run.bat
└── README.md
```

---

## 📋 Eğitim Modülleri (Detay)

### Analiz Dokümanı — Şablon Bölümleri

Sektörde standart BRD (Business Requirements Document) + SRS (Software Requirements Specification) hibrit yapısı:

1. Doküman Bilgileri (versiyon, hazırlayan, tarih)
2. Yönetici Özeti
3. Amaç ve Kapsam (Kapsam Dışı dahil!)
4. Mevcut Durum Analizi
5. Paydaşlar
6. Fonksiyonel Gereksinimler (FG-01..)
7. Fonksiyonel Olmayan Gereksinimler
8. İş Kuralları (IK-01..)
9. Süreç Akışı (Ana + alternatif akışlar)
10. Veri Modeli (yeni tablo/kolon, FK)
11. Kullanıcı Arayüzü / Mock-up
12. Entegrasyonlar
13. Kabul Kriterleri (KK-01..)
14. Test Senaryoları (TS-01: ön koşul / adım / beklenen)
15. Riskler ve Varsayımlar
16. Açık Sorular

### Puanlama Kuralları

**Toplam = (Yapısal + İçerik) / 2**

| Yapısal Skor | Ağırlık |
|---|---|
| Bölüm hiç yok | 0 |
| Yalnız placeholder duruyor | %20 |
| Çok kısa (< yarı min_words) | %50 |
| Kısa (< min_words) | %75 |
| Yeterli (≥ min_words) | %100 |

| İçerik Skoru | Pay |
|---|---|
| Beklenen anahtar kelimeler | %70 |
| Toplam kelime sayısı eşiği | %30 |

---

## 🛠️ Teknolojiler

| Katman | Teknoloji |
|---|---|
| Backend | Python 3.10+ / **FastAPI** 0.115 |
| ASGI Sunucu | Uvicorn |
| Veritabanı | Microsoft **SQL Server** 2019/2022 |
| DB Sürücüsü | pyodbc + ODBC Driver 17 |
| Veri Doğrulama | Pydantic v2 |
| Word İşleme | python-docx (şablon üretme + okuma) |
| Dosya Upload | python-multipart |
| Frontend | Vanilla HTML/CSS/JS (framework yok) |
| API Test | Postman + Swagger UI (otomatik) |

---

## 📜 Lisans & İletişim

Bu proje **eğitim amaçlıdır**. Açık kaynak, MIT benzeri ücretsiz kullanım.

- 👨‍💻 **Hazırlayan**: Ömer Gökdere
- 🎯 **Hedef**: Eren Sarıteke (İş Analisti adayı)
- 🐛 **Hata bildirimi**: GitHub Issues üzerinden
- 💡 **Katkı**: Pull Request'ler memnuniyetle karşılanır

---

> _"Bir iş analistinin en önemli çıktısı yazdığı analiz dokümanıdır. Bu platform, Eren'in o becerisini ölçülebilir egzersizlerle kazanmasını sağlar."_
