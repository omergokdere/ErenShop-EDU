"""
config.py - Uygulama ayarları
.env dosyasından ortam değişkenlerini okur.
"""
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# Veritabanı bağlantı bilgileri
DB_SERVER = os.getenv("DB_SERVER", "localhost")
DB_NAME = os.getenv("DB_NAME", "ErenShopDB")
DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")

# Uygulama ayarları
APP_TITLE = "ErenShop API"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Mini Sipariş ve Stok Yönetim Servisi - Eğitim Projesi"
