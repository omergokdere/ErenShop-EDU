"""
database.py - Veritabanı bağlantı yönetimi
pyodbc kütüphanesi ile MSSQL bağlantısı kurulur.
"""
import pyodbc
from app.config import DB_SERVER, DB_NAME, DB_USER, DB_PASSWORD, DB_DRIVER


def get_connection():
    """
    MSSQL bağlantısı oluşturur ve döndürür.
    
    Windows Authentication (Trusted Connection) kullanılıyorsa:
    - DB_USER ve DB_PASSWORD boş bırakılır
    - connection string'de Trusted_Connection=yes kullanılır
    
    SQL Server Authentication kullanılıyorsa:
    - DB_USER ve DB_PASSWORD .env dosyasına yazılır
    """
    
    # Kullanıcı adı varsa SQL Authentication, yoksa Windows Authentication kullan
    if DB_USER and DB_PASSWORD:
        # SQL Server Authentication
        connection_string = (
            f"DRIVER={{{DB_DRIVER}}};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_NAME};"
            f"UID={DB_USER};"
            f"PWD={DB_PASSWORD};"
        )
    else:
        # Windows Authentication (SSMS'te genellikle bu kullanılır)
        connection_string = (
            f"DRIVER={{{DB_DRIVER}}};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_NAME};"
            f"Trusted_Connection=yes;"
        )
    
    # Bağlantıyı oluştur ve döndür
    connection = pyodbc.connect(connection_string)
    return connection
