-- ============================================================
-- 07_reset_database.sql
-- Veritabanını sıfırlar ve yeniden oluşturur.
-- DİKKAT: Tüm veriler silinir! Sadece eğitim/test ortamında kullan.
-- ============================================================

USE master;
GO

PRINT 'Veritabanı sıfırlanıyor...';

-- Tüm aktif bağlantıları kapat
IF EXISTS (SELECT name FROM sys.databases WHERE name = 'ErenShopDB')
BEGIN
    ALTER DATABASE ErenShopDB SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE ErenShopDB;
    PRINT 'ErenShopDB silindi.';
END

-- Yeni veritabanı oluştur
CREATE DATABASE ErenShopDB;
PRINT 'ErenShopDB yeniden oluşturuldu.';
PRINT '';
PRINT 'Şimdi sırayla şunları çalıştır:';
PRINT '1. 02_create_tables.sql';
PRINT '2. 03_seed_data.sql';
