-- ============================================================
-- 02_create_tables.sql
-- Tüm tabloları oluşturur.
-- Primary Key ve Foreign Key ilişkileri burada tanımlanır.
-- ÖNEMLİ: 01_create_database.sql çalıştırıldıktan sonra çalıştır.
-- ============================================================

USE ErenShopDB;
GO

-- ============================================================
-- 1. Categories Tablosu
-- Ürün kategorilerini tutar.
-- Diğer tablo yok - bağımsız tablo.
-- ============================================================
CREATE TABLE Categories (
    Id          INT IDENTITY(1,1) PRIMARY KEY,  -- Otomatik artan birincil anahtar
    Name        NVARCHAR(100)   NOT NULL,        -- Kategori adı (boş olamaz)
    Description NVARCHAR(500)   NULL,            -- Açıklama (opsiyonel)
    IsActive    BIT             NOT NULL DEFAULT 1,  -- 1=Aktif, 0=Pasif
    CreatedAt   DATETIME        NOT NULL DEFAULT GETDATE(),
    UpdatedAt   DATETIME        NOT NULL DEFAULT GETDATE()
);
PRINT 'Categories tablosu oluşturuldu.';

-- ============================================================
-- 2. Products Tablosu
-- Ürünleri tutar.
-- CategoryId → Categories tablosuna Foreign Key
-- ============================================================
CREATE TABLE Products (
    Id          INT IDENTITY(1,1) PRIMARY KEY,
    CategoryId  INT             NOT NULL,        -- Hangi kategoriye ait?
    Name        NVARCHAR(200)   NOT NULL,
    Description NVARCHAR(1000)  NULL,
    Price       DECIMAL(10,2)   NOT NULL,        -- Para birimi: 10 basamak, 2 ondalık
    Stock       INT             NOT NULL DEFAULT 0,
    IsActive    BIT             NOT NULL DEFAULT 1,
    CreatedAt   DATETIME        NOT NULL DEFAULT GETDATE(),
    UpdatedAt   DATETIME        NOT NULL DEFAULT GETDATE(),

    -- Foreign Key: CategoryId, Categories.Id'ye referans verir
    -- ON DELETE CASCADE: Kategori silinirse ürünler de silinir (dikkatli kullan)
    CONSTRAINT FK_Products_Categories FOREIGN KEY (CategoryId)
        REFERENCES Categories(Id)
);
PRINT 'Products tablosu oluşturuldu.';

-- ============================================================
-- 3. Customers Tablosu
-- Müşterileri tutar.
-- ============================================================
CREATE TABLE Customers (
    Id          INT IDENTITY(1,1) PRIMARY KEY,
    FirstName   NVARCHAR(100)   NOT NULL,
    LastName    NVARCHAR(100)   NOT NULL,
    Email       NVARCHAR(200)   NOT NULL UNIQUE,  -- Email benzersiz olmalı
    Phone       NVARCHAR(20)    NULL,
    Address     NVARCHAR(500)   NULL,
    IsActive    BIT             NOT NULL DEFAULT 1,
    CreatedAt   DATETIME        NOT NULL DEFAULT GETDATE(),
    UpdatedAt   DATETIME        NOT NULL DEFAULT GETDATE()
);
PRINT 'Customers tablosu oluşturuldu.';

-- ============================================================
-- 4. Carts Tablosu
-- Her müşterinin bir aktif sepeti olur.
-- CustomerId → Customers tablosuna Foreign Key
-- ============================================================
CREATE TABLE Carts (
    Id          INT IDENTITY(1,1) PRIMARY KEY,
    CustomerId  INT             NOT NULL,
    IsActive    BIT             NOT NULL DEFAULT 1,
    CreatedAt   DATETIME        NOT NULL DEFAULT GETDATE(),
    UpdatedAt   DATETIME        NOT NULL DEFAULT GETDATE(),

    CONSTRAINT FK_Carts_Customers FOREIGN KEY (CustomerId)
        REFERENCES Customers(Id)
);
PRINT 'Carts tablosu oluşturuldu.';

-- ============================================================
-- 5. CartItems Tablosu
-- Sepetteki ürün satırlarını tutar.
-- CartId → Carts, ProductId → Products
-- ============================================================
CREATE TABLE CartItems (
    Id          INT IDENTITY(1,1) PRIMARY KEY,
    CartId      INT             NOT NULL,
    ProductId   INT             NOT NULL,
    Quantity    INT             NOT NULL DEFAULT 1,
    UnitPrice   DECIMAL(10,2)   NOT NULL,  -- Ürünün o anki fiyatı (fiyat değişse bile korunur)
    CreatedAt   DATETIME        NOT NULL DEFAULT GETDATE(),
    UpdatedAt   DATETIME        NOT NULL DEFAULT GETDATE(), -- Sepet güncellenince bu da güncellenir

    CONSTRAINT FK_CartItems_Carts FOREIGN KEY (CartId)
        REFERENCES Carts(Id),
    CONSTRAINT FK_CartItems_Products FOREIGN KEY (ProductId)
        REFERENCES Products(Id)
);
PRINT 'CartItems tablosu oluşturuldu.';

-- ============================================================
-- 6. Orders Tablosu
-- Siparişleri tutar.
-- CustomerId → Customers tablosuna Foreign Key
-- ============================================================
CREATE TABLE Orders (
    Id          INT IDENTITY(1,1) PRIMARY KEY,
    CustomerId  INT             NOT NULL,
    OrderNumber NVARCHAR(50)    NOT NULL UNIQUE,  -- Benzersiz sipariş numarası
    TotalAmount DECIMAL(10,2)   NOT NULL,
    Status      NVARCHAR(50)    NOT NULL DEFAULT 'Pending',
    -- Geçerli status değerleri:
    -- Pending, Processing, Shipped, Delivered, Cancelled, Paid, PaymentFailed
    CreatedAt   DATETIME        NOT NULL DEFAULT GETDATE(),
    UpdatedAt   DATETIME        NOT NULL DEFAULT GETDATE(),

    CONSTRAINT FK_Orders_Customers FOREIGN KEY (CustomerId)
        REFERENCES Customers(Id)
);
PRINT 'Orders tablosu oluşturuldu.';

-- ============================================================
-- 7. OrderItems Tablosu
-- Siparişteki ürün satırlarını tutar.
-- OrderId → Orders, ProductId → Products
-- ============================================================
CREATE TABLE OrderItems (
    Id          INT IDENTITY(1,1) PRIMARY KEY,
    OrderId     INT             NOT NULL,
    ProductId   INT             NOT NULL,
    Quantity    INT             NOT NULL,
    UnitPrice   DECIMAL(10,2)   NOT NULL,  -- Sipariş anındaki fiyat (sabitlenir)
    TotalPrice  DECIMAL(10,2)   NOT NULL,  -- Quantity * UnitPrice
    CreatedAt   DATETIME        NOT NULL DEFAULT GETDATE(),

    CONSTRAINT FK_OrderItems_Orders FOREIGN KEY (OrderId)
        REFERENCES Orders(Id),
    CONSTRAINT FK_OrderItems_Products FOREIGN KEY (ProductId)
        REFERENCES Products(Id)
);
PRINT 'OrderItems tablosu oluşturuldu.';

-- ============================================================
-- 8. Payments Tablosu
-- Ödeme kayıtlarını tutar.
-- OrderId → Orders tablosuna Foreign Key
-- ============================================================
CREATE TABLE Payments (
    Id              INT IDENTITY(1,1) PRIMARY KEY,
    OrderId         INT             NOT NULL,
    PaymentType     NVARCHAR(50)    NOT NULL,  -- CreditCard, BankTransfer, Cash...
    Amount          DECIMAL(10,2)   NOT NULL,
    IsSuccessful    BIT             NOT NULL DEFAULT 0,
    TransactionCode NVARCHAR(100)   NULL,
    CreatedAt       DATETIME        NOT NULL DEFAULT GETDATE(),

    CONSTRAINT FK_Payments_Orders FOREIGN KEY (OrderId)
        REFERENCES Orders(Id)
);
PRINT 'Payments tablosu oluşturuldu.';

PRINT '';
PRINT 'Tüm tablolar başarıyla oluşturuldu!';
