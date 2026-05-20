# ErenShop API — Kurulum Kılavuzu

Windows ortamında, VSCode + MSSQL Server + Postman ile adım adım kurulum.

---

## 1. Gerekli Programlar

Aşağıdaki programların kurulu olduğundan emin ol:

| Program | Sürüm | İndirme |
|---------|-------|---------|
| Python | 3.10+ | https://python.org |
| VSCode | Güncel | https://code.visualstudio.com |
| MSSQL Server | 2019/2022 | https://microsoft.com/sql-server |
| MSSQL Management Studio (SSMS) | 19+ | https://aka.ms/ssmsfullsetup |
| Postman | Güncel | https://postman.com |
| ODBC Driver 17 for SQL Server | 17+ | https://aka.ms/downloadmsodbcsql |

> **Not:** ODBC Driver kurulu değilse pyodbc bağlantısı çalışmaz. İndirip kur.

---

## 2. Python Kurulumu

1. https://python.org adresinden Python 3.10 veya üstü sürümü indir
2. Kurulum sırasında **"Add Python to PATH"** seçeneğini mutlaka işaretle
3. Kurulum tamamlanınca PowerShell'i aç ve test et:

```powershell
python --version
pip --version
```

Her ikisi de sürüm numarası gösteriyorsa kurulum başarılı.

---

## 3. VSCode ile Projeyi Açma

1. VSCode'u aç
2. `File → Open Folder` 
3. `erenshop-api` klasörünü seç
4. VSCode Python extension kurulu değilse sol menüden Extensions'a gidip `Python` (Microsoft) extension'ını kur

---

## 4. Sanal Ortam (Virtual Environment) Oluşturma

VSCode'da terminal aç: `Ctrl + ~`

```powershell
# Sanal ortam oluştur
python -m venv venv

# Sanal ortamı aktif et (Windows)
venv\Scripts\activate
```

Terminal başında `(venv)` görünüyorsa aktif demektir:
```
(venv) PS C:\...\erenshop-api>
```

> **Neden sanal ortam?** Projeye özel kütüphaneleri izole eder. Diğer projelerle çakışma olmaz.

---

## 5. requirements.txt ile Bağımlılıkları Yükleme

```powershell
pip install -r requirements.txt
```

Yüklenen başlıca paketler:
- `fastapi` — Web framework
- `uvicorn` — ASGI sunucu
- `pyodbc` — MSSQL bağlantısı
- `python-dotenv` — .env dosyası okuma
- `pydantic` — Veri doğrulama

---

## 6. MSSQL — Veritabanı Oluşturma

1. **SSMS'i aç** (SQL Server Management Studio)
2. Server adını gir (genellikle `localhost` veya `.\SQLEXPRESS`)
3. Windows Authentication veya SQL Authentication ile bağlan
4. **New Query** düğmesine tıkla
5. `sql/01_create_database.sql` dosyasının içeriğini yapıştır
6. **F5** veya **Execute** düğmesine bas
7. "ErenShopDB başarıyla oluşturuldu." mesajını gör

---

## 7. SQL Scriptlerini Sırayla Çalıştırma

**Sıra önemli!** Her script bir öncekinin üzerine inşa edilir.

| Sıra | Dosya | Açıklama |
|------|-------|---------|
| 1 | `01_create_database.sql` | Veritabanı oluştur |
| 2 | `02_create_tables.sql` | Tabloları oluştur |
| 3 | `03_seed_data.sql` | Örnek verileri ekle |

Her script için:
1. SSMS'te `New Query` aç
2. Dosyanın içeriğini yapıştır (veya `File → Open` ile aç)
3. Sol üstten veritabanı seçimini kontrol et: **ErenShopDB**
4. F5 ile çalıştır

---

## 8. .env Dosyasını Hazırlama

`.env.example` dosyasını kopyala ve `.env` adıyla kaydet:

```powershell
copy .env.example .env
```

`.env` dosyasını VSCode'da aç ve düzenle:

```env
# Windows Authentication kullanıyorsan (SSMS'te Windows Auth ile bağlanıyorsan):
DB_SERVER=localhost
DB_NAME=ErenShopDB
DB_USER=
DB_PASSWORD=
DB_DRIVER=ODBC Driver 17 for SQL Server

# SQL Authentication kullanıyorsan:
# DB_SERVER=localhost
# DB_NAME=ErenShopDB
# DB_USER=sa
# DB_PASSWORD=SifreniYaz
# DB_DRIVER=ODBC Driver 17 for SQL Server
```

> **İpucu:** SQL Express kullanıyorsan `DB_SERVER=localhost\SQLEXPRESS` yaz.

---

## 9. API'yi Çalıştırma

> ⚠️ **ÖNEMLİ — Terminal Klasörü**
> Tüm komutları `erenshop-api` klasörü **içinde** çalıştırman gerekiyor.
> VSCode'da `File → Open Folder` ile `erenshop-api` klasörünü açtıktan sonra
> `Ctrl + ~` ile terminal aç. Terminal satırı şöyle görünmeli:
> ```
> PS C:\...\erenshop-api>
> ```
> Eğer `eren_TestAPI>` görünüyorsa şu komutu çalıştır:
> ```powershell
> cd erenshop-api
> ```

### Adım adım başlatma (ilk kez)

```powershell
# 1. Sanal ortamı aktif et
venv\Scripts\activate

# 2. Sunucuyu başlat
uvicorn app.main:app --reload --port 8000
```

Terminalda şunu görmen gerekiyor:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

### Sonraki açılışlarda (kısa yol)

```powershell
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

---

## 10. Swagger Kontrolü

Tarayıcında aç: **http://localhost:8000/docs**

Swagger arayüzünde tüm endpoint'leri göreceksin:
- Her endpoint için açıklama
- Request body ve parametre bilgisi
- "Try it out" butonu ile direkt test imkânı

---

## 11. Postman Collection Import Etme

1. Postman'ı aç
2. Sol menüde **Collections** sekmesine tıkla
3. **Import** düğmesine tıkla
4. `postman/ErenShop_API.postman_collection.json` dosyasını seç
5. Import et

---

## 12. Environment Seçme

1. Postman'ı aç
2. Sol menüde **Environments** sekmesine tıkla
3. **Import** ile `postman/ErenShop_Local.postman_environment.json` dosyasını import et
4. Sağ üst köşeden **ErenShop_Local** environment'ını seç

Environment değişkenleri:
- `baseUrl` = http://localhost:8000
- `categoryId`, `productId`, `customerId`, `orderId` vb.

---

## 13. İlk Test İsteğini Atma

1. Collections → ErenShop API → 01 - Health Check → **API Health Check**
2. **Send** butonuna bas
3. Cevap:
```json
{
  "success": true,
  "message": "API ve veritabanı bağlantısı sağlıklı.",
  "data": {
    "api": "ok",
    "database": "ok"
  }
}
```

Tebrikler! API çalışıyor.

---

## 14. SQL Üzerinden Sonucu Kontrol Etme

Postman'dan POST /api/categories ile bir kategori ekledikten sonra SSMS'te kontrol et:

```sql
USE ErenShopDB;
SELECT * FROM Categories;
```

Postman'dan eklediğin kategoriyi tabloda göreceksin. API → DB bağlantısı bu şekilde test edilir.

---

## 15. Sık Karşılaşılan Hatalar ve Çözümleri

### Hata: `pyodbc.InterfaceError: ('IM002', ...)`
**Sebep:** ODBC Driver kurulu değil.  
**Çözüm:** "ODBC Driver 17 for SQL Server" indir ve kur. https://aka.ms/downloadmsodbcsql

---

### Hata: `Login failed for user`
**Sebep:** SQL Server kullanıcı adı veya şifre yanlış.  
**Çözüm:** `.env` dosyasındaki `DB_USER` ve `DB_PASSWORD` değerlerini kontrol et.

---

### Hata: `Cannot open database "ErenShopDB"`
**Sebep:** Veritabanı oluşturulmamış.  
**Çözüm:** SSMS'te `01_create_database.sql` scriptini çalıştır.

---

### Hata: `Address already in use` (port 8000)
**Sebep:** Port zaten kullanılıyor.  
**Çözüm:** `run.bat` içinde port numarasını değiştir (örn. 8001) veya kullanan uygulamayı kapat.

---

### Hata: `ModuleNotFoundError: No module named 'fastapi'`
**Sebep:** Sanal ortam aktif değil veya paketler yüklenmemiş.  
**Çözüm:**  
```powershell
venv\Scripts\activate
pip install -r requirements.txt
```

---

### Hata: `422 Unprocessable Entity` Postman'dan
**Sebep:** Request body formatı yanlış.  
**Çözüm:** Body'nin Content-Type header'ını `application/json` yap. Swagger'da örnek format var.
