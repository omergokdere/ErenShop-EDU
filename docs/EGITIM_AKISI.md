# ErenShop API — 5 Günlük Eğitim Akışı

Her günün sonunda neyi öğrendiğini ve nasıl test edebileceğini göreceksin.

---

## 1. Gün — SQL ve Veritabanı Temelleri

**Öğrenilecekler:**
- MSSQL Management Studio kullanımı
- Database ve tablo oluşturma
- Primary Key, Foreign Key mantığı
- Temel SQL sorguları: SELECT, INSERT, UPDATE, DELETE

---

### Görev Listesi

**1. ErenShopDB'yi oluştur**
1. SSMS'i aç, sunucuya bağlan
2. `sql/01_create_database.sql` dosyasını aç ve çalıştır
3. Sol panelde "ErenShopDB" görünüyor mu? ✓

**2. Tabloları oluştur**
1. `sql/02_create_tables.sql` dosyasını çalıştır
2. SSMS → ErenShopDB → Tables → tüm tabloları gör ✓

**3. Örnek verileri ekle**
1. `sql/03_seed_data.sql` dosyasını çalıştır

**4. SELECT sorguları çalıştır** (`04_training_select_queries.sql`)

Sırayla çalıştır ve sonuçlara bak:
```sql
-- Tüm ürünleri gör
SELECT * FROM Products;

-- Aktif ürünleri filtrele
SELECT * FROM Products WHERE IsActive = 1;

-- Fiyata göre sırala
SELECT Name, Price FROM Products ORDER BY Price DESC;

-- Stok azalan ürünler
SELECT Name, Stock FROM Products WHERE Stock < 10;
```

**5. INSERT/UPDATE/DELETE dene**
```sql
-- Yeni kategori ekle
INSERT INTO Categories (Name, Description, IsActive, CreatedAt, UpdatedAt)
VALUES ('Test Kategori', 'Deneme', 1, GETDATE(), GETDATE());

-- Güncelle
UPDATE Categories SET Name = 'Test 2' WHERE Name = 'Test Kategori';

-- Sil
DELETE FROM Categories WHERE Name = 'Test 2';
```

**Gün Sonu Kontrol:**
- [ ] ErenShopDB oluşturuldu
- [ ] 8 tablo oluşturuldu
- [ ] SELECT ile veriler görüntülendi
- [ ] INSERT/UPDATE/DELETE yapıldı

---

## 2. Gün — API'yi Çalıştırma ve GET Endpoint'leri

**Öğrenilecekler:**
- Python sanal ortam kurulumu
- FastAPI uygulamasını çalıştırma
- Swagger arayüzü inceleme
- Postman collection kullanımı
- GET endpoint'leri test etme

---

### Görev Listesi

**1. Kurulum**
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**2. .env dosyasını ayarla**
```
copy .env.example .env
# .env dosyasını düzenle
```

**3. API'yi başlat**
```powershell
.\run.bat
```

**4. Swagger'ı incele**
- Tarayıcı: http://localhost:8000/docs
- Her endpoint'i incele
- "Try it out" ile birkaç istek dene

**5. Postman kurulumu**
- Collection import et: `postman/ErenShop_API.postman_collection.json`
- Environment import et: `postman/ErenShop_Local.postman_environment.json`
- ErenShop_Local environment'ını seç

**6. GET isteklerini test et**
Sırayla dene:
- `GET /api/health` → API çalışıyor mu?
- `GET /api/categories` → Kategorileri gör
- `GET /api/products` → Ürünleri gör
- `GET /api/customers` → Müşterileri gör
- `GET /api/products/search?keyword=mouse` → Arama dene
- `GET /api/products/category/1` → Kategoriye göre filtrele

**7. SQL ile karşılaştır**
Her Postman isteğinden sonra SSMS'te kontrol et:
```sql
SELECT * FROM Products WHERE CategoryId = 1;
```
Postman ve SQL aynı verileri gösteriyor mu?

**Gün Sonu Kontrol:**
- [ ] API ayakta (run.bat çalışıyor)
- [ ] Swagger açılıyor
- [ ] Postman collection import edildi
- [ ] GET istekleri başarılı
- [ ] SQL ile cevaplar doğrulandı

---

## 3. Gün — POST, PUT, DELETE İstekleri

**Öğrenilecekler:**
- POST ile yeni kayıt oluşturma
- PUT ile güncelleme
- DELETE ile silme
- Request body formatı
- HTTP status kodları

---

### Görev Listesi

**1. Yeni kategori ekle**
- POST /api/categories
- Body: `{"name": "Oyun", "description": "Gaming ürünleri"}`
- 201 Created cevabı gelmeli
- SSMS'te: `SELECT * FROM Categories;` → Yeni kategori var mı?

**2. Yeni ürün ekle**
- POST /api/products
- Body:
```json
{
  "categoryId": 1,
  "name": "Gaming Mouse",
  "description": "12000 DPI gaming mouse",
  "price": 850.00,
  "stock": 15
}
```
- SSMS'te stok ve fiyatı kontrol et

**3. Yeni müşteri ekle**
- POST /api/customers
- Body:
```json
{
  "first_name": "Elif",
  "last_name": "Şahin",
  "email": "elif@test.com",
  "phone": "05551234567",
  "address": "İzmir"
}
```

**4. Güncelleme yap**
- PUT /api/products/1
- Body: `{"price": 499.00, "stock": 50}`
- Sonra GET /api/products/1 ile kontrol et
- SSMS'te de kontrol et: `SELECT Price, Stock FROM Products WHERE Id = 1;`

**5. Silme dene (soft delete)**
- DELETE /api/categories/6 (az önce eklediğin "Oyun" kategorisi)
- Sonra GET /api/categories ile kontrol et → görünmemeli
- SSMS'te kontrol et:
```sql
SELECT * FROM Categories WHERE IsActive = 0;  -- Pasif kayıtlar
```
Fiziksel olarak silinmedi, IsActive = 0 yapıldı!

**6. Hata senaryoları dene**
- GET /api/products/9999 → 404 Not Found
- POST /api/customers ile aynı email'i tekrar dene → 400 Bad Request

**Gün Sonu Kontrol:**
- [ ] POST ile kayıt oluşturuldu
- [ ] PUT ile güncelleme yapıldı
- [ ] DELETE çalışıyor (soft delete)
- [ ] SQL ile sonuçlar doğrulandı
- [ ] 404 ve 400 hatalarını gördün

---

## 4. Gün — Sepet, Sipariş ve Transaction

**Öğrenilecekler:**
- Sepet işlemleri
- Transaction mantığı
- Stok düşme senaryosu
- Hatalı akış senaryoları

---

### Görev Listesi

**1. Sepete ürün ekle**
- POST /api/cart/add
- Body: `{"customerId": 1, "productId": 1, "quantity": 2}`
- Başarılı sepet cevabı gelecek

**2. Sepeti görüntüle**
- GET /api/cart/1
- Ürünler ve toplam tutar görünmeli

**3. Stok durumunu not al**
SSMS'te:
```sql
SELECT Id, Name, Stock FROM Products WHERE Id = 1;
```
Şu anki stoğu yaz: ____

**4. Sipariş oluştur**
- POST /api/orders/create-from-cart
- Body: `{"customerId": 1}`

**5. Transaction etkisini gözlemle**
SSMS'te tekrar kontrol et:
```sql
SELECT Id, Name, Stock FROM Products WHERE Id = 1;
```
Stok düştü mü? ✓

Sepet temizlendi mi?
```sql
SELECT * FROM CartItems;
```

Sipariş oluştu mu?
```sql
SELECT * FROM Orders;
SELECT * FROM OrderItems;
```

**6. Başarısız sipariş senaryosu (stok yetersiz)**
- Önce stoku 0 yap:
```sql
UPDATE Products SET Stock = 0 WHERE Id = 2;
```
- Müşteri 2'nin sepetine ürün 2'yi ekle
- Sipariş oluşturmaya çalış → 400 hatası almalısın!

**7. Ödeme simülasyonu**

Önce başarılı ödeme:
- POST /api/payments/mock-pay
- Body: `{"orderId": 1, "paymentType": "CreditCard", "amount": 900, "forceFail": false}`
- SSMS: `SELECT Status FROM Orders WHERE Id = 1;` → "Paid" olmalı

Başarısız ödeme (yeni sipariş oluşturduktan sonra):
- Body: `{"orderId": 2, "paymentType": "CreditCard", "amount": 500, "forceFail": true}`
- SSMS: `SELECT Status FROM Orders WHERE Id = 2;` → "PaymentFailed" olmalı

**Gün Sonu Kontrol:**
- [ ] Sepet işlemleri çalışıyor
- [ ] Sipariş oluşturulunca stok düşüyor
- [ ] Sepet temizleniyor
- [ ] Başarılı ödeme → "Paid"
- [ ] Başarısız ödeme → "PaymentFailed"
- [ ] Yetersiz stok → 400 hatası

---

## 5. Gün — Raporlar, JOIN Sorguları ve Genel Tekrar

**Öğrenilecekler:**
- Rapor endpoint'leri
- JOIN ve GROUP BY sorguları SQL'de
- Tüm endpoint'lerin genel tekrarı

---

### Görev Listesi

**1. Rapor endpoint'lerini test et**
- GET /api/reports/daily-sales
- GET /api/reports/top-products?limit=5
- GET /api/reports/category-sales
- GET /api/reports/low-stock-products?threshold=20
- GET /api/reports/customer-summary/1

**2. SQL raporlama sorgularını çalıştır** (`06_training_report_queries.sql`)

Her sorguyu tek tek çalıştır:
```sql
-- Günlük satış
SELECT CAST(CreatedAt AS DATE), COUNT(*), SUM(TotalAmount)
FROM Orders WHERE Status = 'Paid'
GROUP BY CAST(CreatedAt AS DATE);

-- En çok satılan ürünler
SELECT TOP 5 p.Name, SUM(oi.Quantity) as Sold
FROM OrderItems oi
INNER JOIN Products p ON oi.ProductId = p.Id
GROUP BY p.Id, p.Name
ORDER BY Sold DESC;
```

**3. JOIN sorgularını çalıştır** (`05_training_join_queries.sql`)
- Ürünleri kategori adıyla getir
- Siparişleri müşteri adıyla getir
- Sipariş detaylarını ürün adıyla getir

**4. Postman Error Scenarios klasörünü bitir**
- 09 - Error Scenarios içindeki tüm hata senaryolarını dene
- Her birinde ne tür cevap geldiğini not al

**5. Genel tekrar — kendini test et**

Aşağıdakileri sıfırdan yapabilir misin?
- [ ] Yeni bir kategori oluştur
- [ ] O kategoriye 2 ürün ekle
- [ ] Yeni bir müşteri oluştur
- [ ] Müşterinin sepetine her iki ürünü ekle
- [ ] Sepetten sipariş oluştur
- [ ] Ödemeyi tamamla
- [ ] Raporlarda siparişi gör
- [ ] Tüm adımları SQL ile doğrula

**Gün Sonu Kontrol:**
- [ ] Tüm rapor endpoint'leri test edildi
- [ ] JOIN sorguları anlaşıldı
- [ ] GROUP BY mantığı kavrandı
- [ ] Hata senaryoları denendi
- [ ] Uçtan uca akış başarıyla tamamlandı

---

## Sonraki Adımlar (Bonus)

Projeyi tamamladıktan sonra bunları dene:

1. **Yeni bir endpoint ekle:** Örneğin `GET /api/products/out-of-stock` (stoksuz ürünler)
2. **Authentication ekle:** JWT token ile giriş sistemi
3. **Pagination ekle:** `/api/products?page=1&size=10`
4. **Logging ekle:** Her istek loglanacak
5. **Deployment:** Uygulamayı bir sunucuya taşı
