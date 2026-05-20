# ErenShop API — API Dökümanı

Tüm endpoint'lerin açıklaması, parametreleri ve örnek cevapları.

---

## Standart Response Formatı

Her API cevabı aynı formatta döner:

**Başarılı:**
```json
{
  "success": true,
  "message": "İşlem başarılı.",
  "data": {}
}
```

**Hatalı:**
```json
{
  "success": false,
  "message": "Hata açıklaması.",
  "data": null
}
```

---

## HTTP Status Kodları

| Kod | Anlam | Ne zaman? |
|-----|-------|-----------|
| 200 | OK | Başarılı GET, PUT, DELETE |
| 201 | Created | Başarılı POST (yeni kayıt) |
| 400 | Bad Request | Geçersiz istek, iş kuralı hatası |
| 404 | Not Found | Kayıt bulunamadı |
| 422 | Unprocessable Entity | Body format hatası (Pydantic) |
| 500 | Internal Server Error | Beklenmedik sunucu hatası |

---

## 1. Health Check

### `GET /api/health`
API ve veritabanı durumunu kontrol eder.

**Cevap:**
```json
{
  "success": true,
  "message": "API ve veritabanı bağlantısı sağlıklı.",
  "data": { "api": "ok", "database": "ok" }
}
```

---

## 2. Categories

### `GET /api/categories`
Tüm aktif kategorileri listeler.

### `GET /api/categories/{category_id}`
Tek kategori getirir.

**Path Parameter:** `category_id` (integer)

### `POST /api/categories`
Yeni kategori ekler.

**Request Body:**
```json
{
  "name": "Elektronik",
  "description": "Elektronik ürünler"
}
```

### `PUT /api/categories/{category_id}`
Kategori günceller. Tüm alanlar opsiyonel.

**Request Body:**
```json
{
  "name": "Yeni Ad",
  "description": "Yeni açıklama",
  "is_active": true
}
```

### `DELETE /api/categories/{category_id}`
Kategoriyi pasife alır (soft delete).

---

## 3. Products

### `GET /api/products`
Tüm aktif ürünleri listeler.

### `GET /api/products/search?keyword=mouse`
Ürün adı ve açıklamasında arama yapar.

**Query Parameter:** `keyword` (string, zorunlu)

### `GET /api/products/category/{category_id}`
Kategoriye göre ürünleri listeler.

### `GET /api/products/{product_id}`
Tek ürün getirir.

### `POST /api/products`
Yeni ürün ekler.

**Request Body:**
```json
{
  "categoryId": 1,
  "name": "Kablosuz Mouse",
  "description": "Bluetooth destekli kablosuz mouse",
  "price": 450.00,
  "stock": 25
}
```

### `PUT /api/products/{product_id}`
Ürün günceller. Tüm alanlar opsiyonel.

### `DELETE /api/products/{product_id}`
Ürünü pasife alır.

---

## 4. Customers

### `GET /api/customers`
Tüm aktif müşterileri listeler.

### `GET /api/customers/{customer_id}`
Tek müşteri getirir.

### `POST /api/customers`
Yeni müşteri ekler. Email benzersiz olmalı.

**Request Body:**
```json
{
  "first_name": "Eren",
  "last_name": "Gokdere",
  "email": "eren@example.com",
  "phone": "05550000000",
  "address": "İstanbul"
}
```

### `PUT /api/customers/{customer_id}`
Müşteri günceller.

### `DELETE /api/customers/{customer_id}`
Müşteriyi pasife alır.

### `GET /api/customers/{customer_id}/orders`
Müşteriye ait siparişleri listeler.

---

## 5. Cart

### `POST /api/cart/add`
Sepete ürün ekler. Müşterinin sepeti yoksa otomatik oluşturur.

**Request Body:**
```json
{
  "customerId": 1,
  "productId": 1,
  "quantity": 2
}
```

**İş Kuralları:**
- Müşteri aktif olmalı
- Ürün aktif olmalı
- Stok yeterli olmalı
- Ürün zaten sepetteyse miktar güncellenir

### `GET /api/cart/{customer_id}`
Müşterinin sepetini ve toplam tutarı getirir.

**Örnek Cevap:**
```json
{
  "success": true,
  "message": "İşlem başarılı.",
  "data": {
    "cart_id": 1,
    "customer_id": 1,
    "items": [
      {
        "CartItemId": 1,
        "ProductId": 1,
        "ProductName": "Kablosuz Mouse",
        "Quantity": 2,
        "UnitPrice": 450.00,
        "LineTotal": 900.00
      }
    ],
    "total": 900.00
  }
}
```

### `DELETE /api/cart/items/{cart_item_id}`
Sepetten tek bir ürünü siler.

### `DELETE /api/cart/clear/{customer_id}`
Sepeti tamamen temizler.

---

## 6. Orders

### `POST /api/orders/create-from-cart`
Müşterinin sepetini siparişe dönüştürür.

**Request Body:**
```json
{
  "customerId": 1
}
```

**İş Kuralları:**
- Müşteri aktif olmalı
- Sepet boş olmamalı
- Tüm ürünler aktif olmalı
- Tüm ürünlerin stoğu yeterli olmalı
- Transaction: tüm adımlar ya hep başarılı ya hep başarısız

**Başarılı sipariş sonrası:**
- Stok otomatik düşer
- Sepet temizlenir
- Sipariş durumu `Pending` olur

### `GET /api/orders`
Tüm siparişleri listeler.

### `GET /api/orders/{order_id}`
Sipariş detayını ve ürün listesini getirir.

### `GET /api/orders/customer/{customer_id}`
Müşteriye ait siparişleri listeler.

### `PUT /api/orders/{order_id}/status`
Sipariş durumunu günceller.

**Request Body:**
```json
{
  "status": "Processing"
}
```

**Geçerli Durumlar:**
`Pending` → `Processing` → `Shipped` → `Delivered`  
`Paid` (ödeme sonrası otomatik)  
`PaymentFailed` (başarısız ödeme sonrası)  
`Cancelled`

---

## 7. Payments

### `POST /api/payments/mock-pay`
Mock ödeme işlemi yapar.

**Request Body:**
```json
{
  "orderId": 1,
  "paymentType": "CreditCard",
  "amount": 900.00,
  "forceFail": false
}
```

**Parametreler:**
- `paymentType`: CreditCard, BankTransfer, Cash (serbest metin)
- `forceFail`: `false` → başarılı, `true` → başarısız simülasyon

**Başarılı Ödeme:**
- `Payments` tablosuna kayıt eklenir
- Sipariş durumu `Paid` olur

**Başarısız Ödeme:**
- `Payments` tablosuna başarısız kayıt eklenir
- Sipariş durumu `PaymentFailed` olur

---

## 8. Reports

### `GET /api/reports/daily-sales`
Günlük satış raporu.

**Query Parameter:** `date` (opsiyonel, format: `YYYY-MM-DD`)  
Verilmezse bugün kullanılır.

### `GET /api/reports/top-products`
En çok satılan ürünler.

**Query Parameter:** `limit` (opsiyonel, varsayılan: 10)

### `GET /api/reports/customer-summary/{customer_id}`
Müşterinin sipariş ve harcama özeti.

### `GET /api/reports/category-sales`
Kategori bazında satış özeti.

### `GET /api/reports/low-stock-products`
Stoğu azalan ürünler.

**Query Parameter:** `threshold` (opsiyonel, varsayılan: 10)
