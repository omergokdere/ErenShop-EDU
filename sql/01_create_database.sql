-- ============================================================
-- 01_create_database.sql
-- ErenShopDB veritabanını oluşturur.
-- MSSQL Management Studio'da bu scripti çalıştır.
-- ============================================================

-- Eğer veritabanı zaten varsa silip yeniden oluştur
-- (Sadece geliştirme/eğitim ortamında kullan!)
IF EXISTS (SELECT name FROM sys.databases WHERE name = 'ErenShopDB')
BEGIN
    -- Aktif bağlantıları kapat ve veritabanını sil
    ALTER DATABASE ErenShopDB SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE ErenShopDB;
    PRINT 'Mevcut ErenShopDB silindi.';
END

-- Yeni veritabanını oluştur
CREATE DATABASE ErenShopDB;
PRINT 'ErenShopDB başarıyla oluşturuldu.';
GO

-- Çalışma veritabanını ErenShopDB olarak ayarla
USE ErenShopDB;
PRINT 'ErenShopDB kullanılıyor.';
