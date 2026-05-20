# ErenShop API — Postman Eğitim Notları

Postman ile API test etmeyi adım adım öğren.

---

## Postman Nedir?

Postman, API'lere HTTP istekleri atmana yarayan araçtır. Tarayıcıda yapamayacağın POST, PUT, DELETE gibi istekleri kolayca atabilirsin.

---

## 1. Temel Kavramlar

### HTTP Metodları

| Metod | Ne yapar? | Örnek |
|-------|-----------|-------|
| GET | Veri okur | Ürün listesi getir |
| POST | Yeni kayıt oluşturur | Ürün ekle |
| PUT | Mevcut kaydı günceller | Ürün fiyatını değiştir |
| DELETE | Kaydı siler/pasife alır | Ürünü sil |

### URL Yapısı

```
http://localhost:8000/api/products/1
       ↑              ↑        ↑
    sunucu         prefix   path param
```

---

## 2. Environment Variable Kullanımı

Environment değişkenleri, URL'leri hardcode yazmak yerine değişken kullanmana yarar.

**Örnek:**
- `{{baseUrl}}` → `http://localhost:8000`
- `{{productId}}` → `1`

**Kullanım:**
```
{{baseUrl}}/api/products/{{productId}}
↓ çalışınca ↓
http://localhost:8000/api/products/1
```

**Değişken nasıl değiştirilir?**
1. Sağ üstte Environment selector → ErenShop_Local
2. Göz simgesine tıkla → değerleri düzenle

---

## 3. İlk İstek: Health Check

1. Collections → 01 - Health Check → API Health Check
2. Method: `GET`
3. URL: `{{baseUrl}}/api/health`
4. **Send** tıkla
5. Response'a bak

```json
{
  "success": true,
  "message": "API ve veritabanı bağlantısı sağlıklı.",
  "data": { "api": "ok", "database": "ok" }
}
```

---

## 4. Query Parameter Kullanımı

URL'nin `?` işaretinden sonra gelen parametreler.

**Örnek:** Ürün arama
```
GET /api/products/search?keyword=mouse
```

Postman'da:
1. URL: `{{baseUrl}}/api/products/search`
2. **Params** sekmesine tıkla
3. Key: `keyword`, Value: `mouse` yaz
4. Send

---

## 5. Path Parameter Kullanımı

URL'nin içinde bulunan parametreler.

**Örnek:** Tek ürün getirme
```
GET /api/products/1
```

Buradaki `1` path parameter'dır.

Postman'da:
1. URL: `{{baseUrl}}/api/products/{{productId}}`
2. `productId` environment variable olarak `1` ayarlı
3. Send

---

## 6. Request Body Gönderme (POST/PUT)

1. Method: `POST` seç
2. URL: `{{baseUrl}}/api/products`
3. **Body** sekmesine tıkla
4. **raw** seç
5. Dropdown'dan **JSON** seç
6. Body içine yaz:

```json
{
  "categoryId": 1,
  "name": "Test Ürün",
  "description": "Açıklama",
  "price": 100.00,
  "stock": 10
}
```

7. Send

---

## 7. Response'u Okuma

**Status Code:** Response'un sağ üstünde
- `200 OK` → Başarılı
- `201 Created` → Yeni kayıt oluşturuldu
- `400 Bad Request` → Hatalı istek
- `404 Not Found` → Kayıt bulunamadı

**Response Body:** JSON formatında döner
```json
{
  "success": true,
  "message": "Ürün başarıyla eklendi.",
  "data": {
    "Id": 17,
    "Name": "Test Ürün",
    ...
  }
}
```

---

## 8. Tam Senaryo: Alışveriş Akışı

Adım adım şu sırayla dene:

### Adım 1: Kategori Ekle
- POST /api/categories
- Body: `{"name": "Test Kategori", "description": "test"}`
- Not: Dönen `Id` değerini `categoryId` variable'ına yaz

### Adım 2: Ürün Ekle
- POST /api/products  
- Body: `{"categoryId": 1, "name": "Test Ürün", "price": 100, "stock": 10}`
- Not: Dönen `Id` değerini `productId` variable'ına yaz

### Adım 3: Müşteri Ekle
- POST /api/customers
- Body: `{"first_name": "Test", "last_name": "User", "email": "test@test.com"}`
- Not: Dönen `Id` değerini `customerId` variable'ına yaz

### Adım 4: Sepete Ürün Ekle
- POST /api/cart/add
- Body: `{"customerId": 1, "productId": 1, "quantity": 2}`

### Adım 5: Sepeti Görüntüle
- GET /api/cart/1
- Toplam tutar görünmeli

### Adım 6: Sipariş Oluştur
- POST /api/orders/create-from-cart
- Body: `{"customerId": 1}`
- Sipariş oluşur, stok düşer, sepet temizlenir

### Adım 7: Ödeme Yap
- POST /api/payments/mock-pay
- Body: `{"orderId": 1, "paymentType": "CreditCard", "amount": 200, "forceFail": false}`
- Sipariş durumu "Paid" olur

### Adım 8: Raporları Gör
- GET /api/reports/top-products
- GET /api/reports/daily-sales

---

## 9. Hata Senaryolarını Test Et

**09 - Error Scenarios** klasörü hata durumlarını içerir.

Bunları deneyerek öğren:

| Senaryo | Beklenen Hata |
|---------|--------------|
| Olmayan kategori ID | 404 Not Found |
| Boş sepetten sipariş | 400 Bad Request |
| Geçersiz sipariş durumu | 400 Bad Request |
| Aynı email ile müşteri ekle | 400 Bad Request |

---

## 10. Headers

Bazı API'ler token veya özel header ister.

ErenShop API'sinde POST/PUT isteklerinde:
```
Content-Type: application/json
```

Header eklemek için:
1. **Headers** sekmesine tıkla
2. Key: `Content-Type`, Value: `application/json`

> Not: Body → raw → JSON seçilince bu header otomatik eklenir.
