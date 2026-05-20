# ErenShop API

**Mini Sipariş ve Stok Yönetim Servisi — Eğitim Projesi**

Python FastAPI + Microsoft SQL Server ile geliştirilmiş, eğitim amaçlı bir backend API projesidir.

## Proje Amacı

Bu proje, başlangıç/orta seviye geliştiricilerin şunları öğrenmesi için hazırlanmıştır:

- MSSQL'de veritabanı ve tablo oluşturma
- Primary Key ve Foreign Key ilişkileri
- SQL: SELECT, INSERT, UPDATE, DELETE, JOIN, GROUP BY
- FastAPI ile REST API geliştirme
- GET, POST, PUT, DELETE metodları
- Postman ile API testi
- Transaction mantığı
- Hata yönetimi ve HTTP status kodları
- Swagger arayüzü ile API inceleme

## Teknolojiler

| Katman | Teknoloji |
|--------|-----------|
| Backend | Python 3.10+ / FastAPI |
| Veritabanı | Microsoft SQL Server |
| DB Bağlantısı | pyodbc |
| API Testi | Postman |
| Dokümantasyon | Swagger (otomatik) + Markdown |

## Hızlı Başlangıç

```bash
# 1. Sanal ortam oluştur
python -m venv venv
venv\Scripts\activate

# 2. Bağımlılıkları yükle
pip install -r requirements.txt

# 3. .env dosyasını ayarla
copy .env.example .env
# .env dosyasını düzenle

# 4. SQL scriptlerini çalıştır (SSMS'te sırayla)
# sql/01_create_database.sql
# sql/02_create_tables.sql
# sql/03_seed_data.sql

# 5. API'yi başlat
run.bat
# veya: uvicorn app.main:app --reload
```

## Swagger

API çalışınca → [http://localhost:8000/docs](http://localhost:8000/docs)

## Modüller

| Modül | Endpoint Sayısı |
|-------|----------------|
| Health | 1 |
| Categories | 5 |
| Products | 7 |
| Customers | 6 |
| Cart | 4 |
| Orders | 5 |
| Payments | 1 |
| Reports | 5 |

## Klasör Yapısı

```
erenshop-api/
├── app/
│   ├── main.py          → FastAPI başlangıç noktası
│   ├── database.py      → MSSQL bağlantısı
│   ├── config.py        → Ayarlar
│   ├── routes/          → Endpoint tanımları
│   ├── schemas/         → Veri modelleri (Pydantic)
│   ├── services/        → İş mantığı + SQL sorguları
│   └── utils/           → Yardımcı fonksiyonlar
├── sql/                 → MSSQL scriptleri
├── postman/             → Postman collection + environment
├── docs/                → Dokümantasyon
├── requirements.txt
├── .env.example
└── run.bat
```

## Detaylı Dokümantasyon

- [Kurulum Kılavuzu](KURULUM.md)
- [API Dökümanı](API_DOKUMANI.md)
- [SQL Eğitim Notları](SQL_EGITIM_NOTLARI.md)
- [Postman Eğitim Notları](POSTMAN_EGITIM_NOTLARI.md)
- [Eğitim Akışı (5 Günlük Plan)](EGITIM_AKISI.md)
