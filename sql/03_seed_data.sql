-- ============================================================
-- 03_seed_data.sql
-- Örnek veriler ekler.
-- ÖNEMLİ: 02_create_tables.sql çalıştırıldıktan sonra çalıştır.
-- ============================================================

USE ErenShopDB;
GO

-- ============================================================
-- Kategoriler
-- ============================================================
INSERT INTO Categories (Name, Description) VALUES
(N'Elektronik', N'Bilgisayar, telefon ve elektronik ürünler'),
(N'Ofis Malzemeleri', N'Kalem, kağıt, dosya ve ofis gereçleri'),
(N'Ev & Yaşam', N'Ev dekorasyon ve yaşam ürünleri'),
(N'Giyim', N'Erkek, kadın ve çocuk giyim ürünleri'),
(N'Spor & Outdoor', N'Spor ekipmanları ve outdoor ürünler');

PRINT 'Kategoriler eklendi.';

-- ============================================================
-- Ürünler
-- ============================================================
-- Elektronik (CategoryId = 1)
INSERT INTO Products (CategoryId, Name, Description, Price, Stock) VALUES
(1, N'Kablosuz Mouse', N'Bluetooth destekli, pil ömrü uzun kablosuz mouse', 450.00, 25),
(1, N'Mekanik Klavye', N'RGB aydınlatmalı mekanik gaming klavye', 1250.00, 15),
(1, N'USB-C Hub', N'7 portlu USB-C çoklayıcı, HDMI ve SD kart okuyucu', 380.00, 40),
(1, N'Kulaklık', N'Gürültü önleyici kablosuz kulaklık', 2100.00, 8),
(1, N'Webcam', N'1080p Full HD webcam, dahili mikrofon', 650.00, 20);

-- Ofis Malzemeleri (CategoryId = 2)
INSERT INTO Products (CategoryId, Name, Description, Price, Stock) VALUES
(2, N'Tükenmez Kalem Seti', N'12 renk tükenmez kalem seti', 45.00, 100),
(2, N'A4 Kağıt (500 Yaprak)', N'Beyaz ofis kağıdı, 80 gr', 120.00, 60),
(2, N'Dosya Düzenleyici', N'Plastik 12 bölmeli dosya düzenleyici', 85.00, 35),
(2, N'Zımba Makinesi', N'Orta boy masaüstü zımba makinesi', 95.00, 25),
(2, N'Not Defteri', N'A5 boyut, 120 sayfa çizgili not defteri', 55.00, 80);

-- Ev & Yaşam (CategoryId = 3)
INSERT INTO Products (CategoryId, Name, Description, Price, Stock) VALUES
(3, N'Masa Lambası', N'LED masa lambası, 3 renk sıcaklığı', 320.00, 18),
(3, N'Çerçeve Set', N'3 lü fotoğraf çerçeve seti, ahşap', 175.00, 30),
(3, N'Bitki Saksısı', N'Seramik saksı, 3 farklı boyut', 95.00, 50);

-- Spor (CategoryId = 5)
INSERT INTO Products (CategoryId, Name, Description, Price, Stock) VALUES
(5, N'Koşu Bandı', N'Katlanabilir ev tipi koşu bandı', 8500.00, 5),
(5, N'Dambıl Seti', N'2x5 kg dambıl seti, kauçuk kaplama', 450.00, 12),
(5, N'Yoga Matı', N'6mm kalınlık, kaymaz taban yoga matı', 180.00, 9);

PRINT 'Ürünler eklendi.';

-- ============================================================
-- Müşteriler
-- ============================================================
INSERT INTO Customers (FirstName, LastName, Email, Phone, Address) VALUES
(N'Eren',    N'Gokdere', N'eren@example.com',   N'05550000001', N'İstanbul, Kadıköy'),
(N'Ayşe',   N'Kaya',    N'ayse@example.com',    N'05550000002', N'Ankara, Çankaya'),
(N'Mehmet',  N'Demir',   N'mehmet@example.com',  N'05550000003', N'İzmir, Bornova'),
(N'Zeynep',  N'Çelik',   N'zeynep@example.com',  N'05550000004', N'Bursa, Osmangazi'),
(N'Ali',     N'Yılmaz',  N'ali@example.com',     N'05550000005', N'Antalya, Muratpaşa');

PRINT 'Müşteriler eklendi.';

-- ============================================================
-- Örnek Sepet (Eren için)
-- ============================================================
INSERT INTO Carts (CustomerId) VALUES (1);  -- Cart Id = 1, CustomerId = 1 (Eren)

INSERT INTO CartItems (CartId, ProductId, Quantity, UnitPrice) VALUES
(1, 1, 2, 450.00),   -- 2 adet Kablosuz Mouse
(1, 3, 1, 380.00);   -- 1 adet USB-C Hub

PRINT 'Örnek sepet eklendi.';

PRINT '';
PRINT 'Tüm örnek veriler başarıyla eklendi!';
PRINT 'Toplam: 5 kategori, 16 ürün, 5 müşteri';
