# ErenShop API — SQL Eğitim Notları

Bu dokümanda öğrendiğin SQL kavramları ve örnekleri açıklanmıştır.

---

## 1. Veritabanı ve Tablo Nedir?

**Veritabanı (Database):** Tablolari içeren konteyner. Bizim veritabanımız: `ErenShopDB`

**Tablo (Table):** Excel tablosu gibi düşün. Sütunlar (kolonlar) ve satırlar (veriler) vardır.

```
Categories Tablosu:
+----+------------+---------------------+----------+
| Id | Name       | Description         | IsActive |
+----+------------+---------------------+----------+
|  1 | Elektronik | Elektronik ürünler  |    1     |
|  2 | Ofis       | Ofis malzemeleri    |    1     |
+----+------------+---------------------+----------+
```

---

## 2. Primary Key (Birincil Anahtar)

Her tablodaki her satırı benzersiz şekilde tanımlar.

```sql
-- Id sütunu PRIMARY KEY'dir
-- IDENTITY(1,1) → otomatik 1'den başlayarak artar
CREATE TABLE Categories (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    ...
);
```

**Kural:** İki satır aynı Id'ye sahip olamaz.

---

## 3. Foreign Key (Yabancı Anahtar)

Bir tablodaki sütunun başka bir tabloya referans vermesidir.

```sql
-- Products.CategoryId → Categories.Id'yi referans alır
-- Yani: Her ürün mutlaka geçerli bir kategoriye ait olmalı
CONSTRAINT FK_Products_Categories FOREIGN KEY (CategoryId)
    REFERENCES Categories(Id)
```

**Görsel:**
```
Categories (Id=1, Name="Elektronik")
     ↑
Products (CategoryId=1, Name="Mouse")
```

---

## 4. Temel SQL Komutları

### SELECT — Veri Okuma
```sql
-- Tüm sütunlar
SELECT * FROM Products;

-- Belirli sütunlar
SELECT Name, Price FROM Products;

-- Koşul ile
SELECT * FROM Products WHERE IsActive = 1;

-- Sıralama
SELECT * FROM Products ORDER BY Price DESC;
```

### INSERT — Veri Ekleme
```sql
INSERT INTO Categories (Name, Description, IsActive, CreatedAt, UpdatedAt)
VALUES ('Elektronik', 'Elektronik ürünler', 1, GETDATE(), GETDATE());
```

### UPDATE — Veri Güncelleme
```sql
-- DİKKAT: WHERE yazmayı unutma! Yoksa tüm satırlar güncellenir!
UPDATE Products
SET Stock = 20, UpdatedAt = GETDATE()
WHERE Id = 1;
```

### DELETE — Veri Silme
```sql
-- DİKKAT: WHERE yazmayı unutma!
DELETE FROM CartItems WHERE CartId = 1;
```

---

## 5. JOIN Kavramı

İki tabloyu birleştirerek sorgulama.

**Neden lazım?** Ürün tablosunda sadece `CategoryId` var, isim yok. İsmi almak için Categories tablosuna bağlanmak gerekir.

```sql
-- Ürünleri kategori adıyla getir
SELECT p.Name, p.Price, c.Name AS CategoryName
FROM Products p
INNER JOIN Categories c ON p.CategoryId = c.Id;
```

```
INNER JOIN: Her iki tabloda da eşleşen kayıtları getirir
LEFT JOIN:  Sol tablonun tüm kayıtları + sağ tabloda eşleşenler
```

---

## 6. Aggregate Fonksiyonlar

```sql
COUNT(*)      -- Kaç satır var?
SUM(Price)    -- Toplamı hesapla
AVG(Price)    -- Ortalamayı hesapla
MIN(Price)    -- En küçük değer
MAX(Price)    -- En büyük değer
```

---

## 7. GROUP BY

Verileri gruplandırarak özet bilgi almak için.

```sql
-- Kategorilere göre ürün sayısı
SELECT CategoryId, COUNT(*) AS ProductCount
FROM Products
GROUP BY CategoryId;

-- Sipariş durumuna göre toplam tutar
SELECT Status, SUM(TotalAmount) AS Total
FROM Orders
GROUP BY Status;
```

**Kural:** SELECT'teki her sütun ya GROUP BY'da olmalı ya da aggregate fonksiyon içinde olmalı.

---

## 8. HAVING

GROUP BY sonrasında filtre uygulamak için. WHERE gruplama öncesi, HAVING gruplama sonrası çalışır.

```sql
-- En az 3 ürünü olan kategoriler
SELECT CategoryId, COUNT(*) AS ProductCount
FROM Products
GROUP BY CategoryId
HAVING COUNT(*) >= 3;
```

---

## 9. Transaction Kavramı

**Transaction:** Birden fazla SQL işleminin "ya hep ya hiç" prensibiyle çalışması.

**Örnek senaryo:** Sipariş oluşturma
1. Orders tablosuna kayıt ekle
2. OrderItems tablosuna satırlar ekle
3. Products tablosundan stok düş
4. CartItems tablosunu temizle

Eğer 3. adımda hata olursa 1. ve 2. adımlar da geri alınmalı. Yarım kalan sipariş olmaz.

```sql
BEGIN TRANSACTION;

BEGIN TRY
    -- Adım 1
    INSERT INTO Orders (...) VALUES (...);
    
    -- Adım 2
    INSERT INTO OrderItems (...) VALUES (...);
    
    -- Adım 3
    UPDATE Products SET Stock = Stock - 1 WHERE Id = 1;
    
    -- Hepsi başarılıysa kaydet
    COMMIT TRANSACTION;
END TRY

BEGIN CATCH
    -- Hata oluştuysa geri al
    ROLLBACK TRANSACTION;
    PRINT 'Hata: ' + ERROR_MESSAGE();
END CATCH;
```

**Python/pyodbc'de Transaction:**
```python
try:
    cursor.execute("INSERT ...")
    cursor.execute("UPDATE ...")
    conn.commit()  # Başarılı → kaydet
except:
    conn.rollback()  # Hata → geri al
```

---

## 10. Soft Delete (Mantıksal Silme)

Veritabanından fiziksel olarak silmek yerine IsActive = 0 yapmak.

```sql
-- Fiziksel silme (DİKKAT: geri dönüşü yok!)
DELETE FROM Products WHERE Id = 1;

-- Soft delete (geri getirilebilir)
UPDATE Products SET IsActive = 0 WHERE Id = 1;
```

**Neden tercih ederiz?**
- Veri kaybı olmaz
- Geçmişi izleyebiliriz
- Siparişlerde bağlantılı ürün hâlâ görünür

---

## 11. Faydalı MSSQL Fonksiyonları

```sql
GETDATE()           -- Şu anki tarih ve saat
CAST(x AS DATE)     -- Tarih-saati sadece tarihe çevir
ISNULL(x, 0)        -- NULL ise 0 kullan
LEN('metin')        -- Metin uzunluğu
UPPER('metin')      -- Büyük harf
LOWER('Metin')      -- Küçük harf
CONCAT(a, ' ', b)   -- Metinleri birleştir
```
