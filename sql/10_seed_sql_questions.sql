-- ============================================================
-- 10_seed_sql_questions.sql
-- ErenShop şeması üzerinden SQL bilgi testi soru bankası.
--   - Difficulty: easy | medium | hard
--   - QuestionType: multiple_choice | fill_in_blank | short_code
--   - OptionsJson: çoktan seçmeli için JSON array ["A","B","C","D"]
--   - CorrectAnswer:
--       multiple_choice  -> şık indeksi "0"|"1"|"2"|"3"
--       fill_in_blank    -> düz metin (case-insensitive ve trim karşılaştırılır)
--       short_code       -> SQL kodu (normalize edilip karşılaştırılır)
-- ============================================================

USE ErenShopDB;
GO

-- Bağımlı kayıtlar varsa yeniden seed atılmaz
IF EXISTS (SELECT 1 FROM SqlTestQuestions)
BEGIN
    PRINT 'SqlTestQuestions kayitlari mevcut, SqlQuestions temizlenmedi.';
    RETURN;
END

IF EXISTS (SELECT 1 FROM SqlQuestions)
BEGIN
    DELETE FROM SqlQuestions;
    DBCC CHECKIDENT ('SqlQuestions', RESEED, 0);
    PRINT 'Eski SqlQuestions kayitlari temizlendi.';
END
GO

-- ============================================================
-- KOLAY SEVİYE (20 soru)
-- ============================================================
INSERT INTO SqlQuestions (QuestionText, QuestionType, Difficulty, OptionsJson, CorrectAnswer, Explanation, Points) VALUES

(N'Bir tablodaki tüm sütunları listelemek için hangi SQL anahtar kelimesi kullanılır?',
 N'multiple_choice', N'easy',
 N'["ALL", "*", "EVERY", "FULL"]',
 N'1',
 N'SELECT * FROM tablo şeklinde * (yıldız) tüm sütunları getirir.', 10),

(N'Products tablosundaki tüm satırları getiren sorguda boşluğu doldurun:  SELECT * ____ Products;',
 N'fill_in_blank', N'easy',
 NULL,
 N'FROM',
 N'FROM anahtar kelimesi hangi tablodan veri çekileceğini belirtir.', 10),

(N'Sadece aktif (IsActive = 1) kategorileri listeleyen SQL sorgusunu yazın.',
 N'short_code', N'easy',
 NULL,
 N'SELECT * FROM Categories WHERE IsActive = 1',
 N'WHERE ile filtre uygulanır. IsActive = 1 aktif kayıtlardır.', 10),

(N'Bir tablodaki kayıt sayısını döndüren fonksiyon hangisidir?',
 N'multiple_choice', N'easy',
 N'["SUM()", "COUNT()", "TOTAL()", "ROWS()"]',
 N'1',
 N'COUNT(*) tablodaki satır sayısını döndürür.', 10),

(N'Products tablosunda fiyatı 100''den büyük ürünleri getiren WHERE koşulunu yazın (sadece WHERE satırı):',
 N'fill_in_blank', N'easy',
 NULL,
 N'WHERE Price > 100',
 N'> operatörü "büyüktür" anlamına gelir.', 10),

(N'Hangi anahtar kelime sonuçları sıralamak için kullanılır?',
 N'multiple_choice', N'easy',
 N'["SORT BY", "ORDER BY", "GROUP BY", "ARRANGE BY"]',
 N'1',
 N'ORDER BY ASC (artan) veya DESC (azalan) ile sıralama yapar.', 10),

(N'Ürünleri fiyata göre AZALAN sırada listeleyen sorguyu yazın (Products tablosundan Name ve Price kolonları):',
 N'short_code', N'easy',
 NULL,
 N'SELECT Name, Price FROM Products ORDER BY Price DESC',
 N'DESC = descending (azalan). ASC = ascending (artan, varsayılan).', 10),

(N'Bir kategoriye yeni kayıt eklemek için kullanılan komut:',
 N'multiple_choice', N'easy',
 N'["ADD INTO", "INSERT INTO", "PUT INTO", "CREATE INTO"]',
 N'1',
 N'INSERT INTO tablo (kolonlar) VALUES (degerler) ile kayıt eklenir.', 10),

(N'Bir kaydı güncellemek için hangi komut kullanılır?',
 N'multiple_choice', N'easy',
 N'["MODIFY", "CHANGE", "UPDATE", "ALTER"]',
 N'2',
 N'UPDATE tablo SET kolon = deger WHERE kosul ile güncelleme yapılır.', 10),

(N'Hangi komut bir kaydı tablodan SİLER?',
 N'multiple_choice', N'easy',
 N'["REMOVE", "ERASE", "DELETE", "DROP"]',
 N'2',
 N'DELETE FROM tablo WHERE kosul. DROP ise tablonun tamamını siler.', 10),

(N'Müşteri tablosunda email değeri "ahmet@test.com" olan kaydı bulan WHERE koşulu nedir?',
 N'fill_in_blank', N'easy',
 NULL,
 N'WHERE Email = ''ahmet@test.com''',
 N'String değerler tek tırnak içinde yazılır.', 10),

(N'NULL değer kontrolü için hangi operatör kullanılır?',
 N'multiple_choice', N'easy',
 N'["= NULL", "IS NULL", "EQUALS NULL", "== NULL"]',
 N'1',
 N'NULL ile = kullanılmaz, IS NULL / IS NOT NULL kullanılır.', 10),

(N'Stoğu 10''dan az olan ürünleri getiren sorguyu yazın:',
 N'short_code', N'easy',
 NULL,
 N'SELECT * FROM Products WHERE Stock < 10',
 N'Karşılaştırma operatörleri: <, >, <=, >=, =, <>', 10),

(N'İlk 5 ürünü getiren sorguda boşluğu doldurun:  SELECT ___ 5 * FROM Products;',
 N'fill_in_blank', N'easy',
 NULL,
 N'TOP',
 N'MSSQL''de TOP N kullanılır. (MySQL''de LIMIT, Oracle''da ROWNUM)', 10),

(N'Customers tablosunda ismi "A" harfi ile başlayanları bulan operatör:',
 N'multiple_choice', N'easy',
 N'["STARTSWITH", "LIKE", "MATCH", "BEGIN"]',
 N'1',
 N'LIKE ''A%'' → A ile başlayanlar. % çoklu karakter, _ tek karakter.', 10),

(N'İki koşulun BİRLİKTE sağlanması için hangi operatör?',
 N'multiple_choice', N'easy',
 N'["OR", "AND", "BOTH", "PLUS"]',
 N'1',
 N'AND her iki koşulun da true olmasını ister; OR herhangi birinin.', 10),

(N'Tekrar eden değerleri tek seferlik göstermek için kullanılan anahtar kelime:',
 N'multiple_choice', N'easy',
 N'["UNIQUE", "DISTINCT", "ONLY", "SINGLE"]',
 N'1',
 N'SELECT DISTINCT Kolon FROM tablo → tekrarsız değer döndürür.', 10),

(N'CategoryId = 1 olan ürünlerin sadece Name ve Price kolonlarını döndüren sorguyu yazın:',
 N'short_code', N'easy',
 NULL,
 N'SELECT Name, Price FROM Products WHERE CategoryId = 1',
 N'İhtiyacınız olan kolonları belirtmek * yerine daha performanslıdır.', 10),

(N'Fiyatı 100 ile 500 arasındaki ürünler için kullanılan operatör (sınırlar dahil):',
 N'multiple_choice', N'easy',
 N'["IN", "BETWEEN", "RANGE", "WITHIN"]',
 N'1',
 N'WHERE Price BETWEEN 100 AND 500 — iki sınır da dahildir.', 10),

(N'Customers tablosunda Phone değeri NULL olan kayıtları bulan WHERE koşulu:',
 N'fill_in_blank', N'easy',
 NULL,
 N'WHERE Phone IS NULL',
 N'NULL kontrolü için IS NULL veya IS NOT NULL kullanılır.', 10),


-- ============================================================
-- ORTA SEVİYE (25 soru)
-- ============================================================

(N'İki tabloyu eşleştirip ortak kayıtları getiren JOIN tipi:',
 N'multiple_choice', N'medium',
 N'["LEFT JOIN", "RIGHT JOIN", "INNER JOIN", "FULL JOIN"]',
 N'2',
 N'INNER JOIN sadece her iki tabloda eşleşen kayıtları döndürür.', 15),

(N'Ürünleri kategori adı ile birlikte getirmek için boşluğu doldurun:  SELECT p.Name, c.Name FROM Products p INNER JOIN Categories c ___ p.CategoryId = c.Id;',
 N'fill_in_blank', N'medium',
 NULL,
 N'ON',
 N'JOIN sonrası ON ile eşleşme koşulu yazılır.', 15),

(N'Sol taraftaki tablonun tüm kayıtlarını, sağdan ise eşleşenleri getiren JOIN:',
 N'multiple_choice', N'medium',
 N'["INNER JOIN", "LEFT JOIN", "CROSS JOIN", "SELF JOIN"]',
 N'1',
 N'LEFT JOIN: solun tüm satırları + sağın eşleşenleri. Eşleşmeyen sağ kolonlar NULL.', 15),

(N'Her kategoriye kaç ürün olduğunu getiren sorguyu yazın (CategoryId ile sayı):',
 N'short_code', N'medium',
 NULL,
 N'SELECT CategoryId, COUNT(*) FROM Products GROUP BY CategoryId',
 N'COUNT(*) aggregate fonksiyondur, GROUP BY ile gruplama gerekir.', 15),

(N'Toplam değer hesaplayan aggregate fonksiyon:',
 N'multiple_choice', N'medium',
 N'["TOTAL()", "ADD()", "SUM()", "PLUS()"]',
 N'2',
 N'SUM() sayısal kolonları toplar.', 15),

(N'Ortalama değer döndüren fonksiyon:',
 N'multiple_choice', N'medium',
 N'["AVG()", "MEAN()", "AVERAGE()", "MID()"]',
 N'0',
 N'AVG() bir sayısal kolonun ortalamasını döndürür.', 15),

(N'En yüksek fiyatı bulan fonksiyon:',
 N'multiple_choice', N'medium',
 N'["TOP()", "HIGH()", "MAX()", "BIG()"]',
 N'2',
 N'MAX() en yüksek, MIN() en düşük değeri döndürür.', 15),

(N'GROUP BY''dan sonra filtreleme yapmak için hangi anahtar kelime kullanılır?',
 N'multiple_choice', N'medium',
 N'["WHERE", "HAVING", "FILTER", "GROUP WHERE"]',
 N'1',
 N'WHERE gruplamadan önce; HAVING gruplandıktan sonra filtreler.', 15),

(N'Birden fazla siparişi olan müşterileri bulan sorguyu yazın (CustomerId ve sayı):',
 N'short_code', N'medium',
 NULL,
 N'SELECT CustomerId, COUNT(*) FROM Orders GROUP BY CustomerId HAVING COUNT(*) > 1',
 N'HAVING ile gruplanmış sonuçlara filtre uygulanır.', 15),

(N'Aşağıdaki sorguda boşluğu doldurun — kategori başına ortalama ürün fiyatı:  SELECT CategoryId, ___(Price) FROM Products GROUP BY CategoryId;',
 N'fill_in_blank', N'medium',
 NULL,
 N'AVG',
 N'AVG fonksiyonu ortalama döndürür.', 15),

(N'Status değeri "Paid" olan siparişlerin toplam tutarını getiren sorguyu yazın:',
 N'short_code', N'medium',
 NULL,
 N'SELECT SUM(TotalAmount) FROM Orders WHERE Status = ''Paid''',
 N'Aggregate fonksiyon + WHERE filtresi birlikte kullanılabilir.', 15),

(N'Bir kolona takma ad (alias) vermek için kullanılan anahtar kelime:',
 N'multiple_choice', N'medium',
 N'["ALIAS", "AS", "RENAME", "NAME"]',
 N'1',
 N'SELECT COUNT(*) AS Toplam FROM tablo şeklinde kullanılır.', 15),

(N'Müşteri başına toplam sipariş tutarını getiren sorguyu yazın (Customers ve Orders JOIN, müşteri adı ile):',
 N'short_code', N'medium',
 NULL,
 N'SELECT c.FirstName, SUM(o.TotalAmount) FROM Customers c INNER JOIN Orders o ON c.Id = o.CustomerId GROUP BY c.FirstName',
 N'JOIN sonrası GROUP BY ile aggregate alınır. Birden fazla kolona göre gruplanabilir.', 20),

(N'Bir tabloyu kendisi ile birleştirmek için kullanılan JOIN türü:',
 N'multiple_choice', N'medium',
 N'["SELF JOIN", "RECURSIVE JOIN", "AUTO JOIN", "LOOP JOIN"]',
 N'0',
 N'SELF JOIN — aynı tabloyu iki kez (farklı alias ile) kullanarak birleştirme.', 15),

(N'Subquery (alt sorgu) nedir?',
 N'multiple_choice', N'medium',
 N'["İki tablo birleştirme", "Bir SQL sorgusu içinde başka bir sorgu", "Stored procedure", "Trigger"]',
 N'1',
 N'Bir sorgunun WHERE, FROM veya SELECT içinde başka bir sorgu kullanmasıdır.', 15),

(N'Aşağıdaki sorgu ne yapar?\nSELECT * FROM Products WHERE Price > (SELECT AVG(Price) FROM Products);',
 N'multiple_choice', N'medium',
 N'["Tüm ürünleri getirir", "Ortalama fiyattan yüksek ürünleri getirir", "Ortalama fiyatı getirir", "En pahalı ürünü getirir"]',
 N'1',
 N'Alt sorgu ortalama fiyatı hesaplar, dış sorgu bundan büyük olanları filtreler.', 20),

(N'IN operatörü ne için kullanılır?',
 N'multiple_choice', N'medium',
 N'["Bir değer listesi içinde kontrol", "Tablodaki sütun listesi", "JOIN yapmak", "GROUP BY alternatifi"]',
 N'0',
 N'WHERE Kolon IN (deger1, deger2, ...) ile çoklu eşleşme kontrolü.', 15),

(N'Aşağıdaki sorguda hata vardır:  SELECT CategoryId, Name, COUNT(*) FROM Products GROUP BY CategoryId; — Hata nedir?',
 N'multiple_choice', N'medium',
 N'["COUNT yanlış", "Name kolonu GROUP BY''a eklenmemiş", "FROM eksik", "Tablo adı yanlış"]',
 N'1',
 N'SELECT''te aggregate olmayan tüm kolonlar GROUP BY''a eklenmek zorundadır.', 20),

(N'Son 7 gün içinde oluşturulmuş siparişleri getiren WHERE koşulunu yazın (CreatedAt kolonu):',
 N'fill_in_blank', N'medium',
 NULL,
 N'WHERE CreatedAt >= DATEADD(DAY, -7, GETDATE())',
 N'DATEADD ile tarihte ileri/geri gidilir. GETDATE() şu anki tarihtir.', 20),

(N'OrderItems tablosunda en çok satılan ürünün ID''sini bulan sorguyu yazın (Quantity toplamı en yüksek):',
 N'short_code', N'medium',
 NULL,
 N'SELECT TOP 1 ProductId, SUM(Quantity) FROM OrderItems GROUP BY ProductId ORDER BY SUM(Quantity) DESC',
 N'TOP 1 + ORDER BY ile en yüksek değerli kayıt alınır.', 20),

(N'UNION ile UNION ALL arasındaki fark nedir?',
 N'multiple_choice', N'medium',
 N'["UNION daha hızlıdır", "UNION ALL tekrarları siler", "UNION tekrarları siler, UNION ALL silmez", "Aynı şeydir"]',
 N'2',
 N'UNION DISTINCT yapar (yavaş), UNION ALL tüm satırları döndürür (hızlı).', 15),

(N'CASE WHEN nedir?',
 N'multiple_choice', N'medium',
 N'["Tablo oluşturma komutu", "Koşullu mantık (if-else benzeri)", "Loop yapısı", "Tetikleyici"]',
 N'1',
 N'CASE WHEN kosul THEN deger ELSE diger END — SELECT içinde kullanılır.', 15),

(N'Ürün stoğunu kategorisine göre "Az/Normal/Yeterli" olarak etiketleyen CASE bloğunu yazın (Stock < 10 Az, 10-50 Normal, > 50 Yeterli):',
 N'short_code', N'medium',
 NULL,
 N'CASE WHEN Stock < 10 THEN ''Az'' WHEN Stock <= 50 THEN ''Normal'' ELSE ''Yeterli'' END',
 N'CASE WHEN ile koşullu değer atanır.', 20),

(N'Tarih farkını gün olarak hesaplayan fonksiyon:',
 N'multiple_choice', N'medium',
 N'["DATEDIFF", "DATEDELTA", "TIMEDIFF", "DAYBETWEEN"]',
 N'0',
 N'DATEDIFF(DAY, baslangic, bitis) iki tarih arasındaki günü döndürür.', 15),

(N'Customers tablosundaki müşterileri en yeni kayıttan eskiye sıralayıp sadece son 10''unu getirin:',
 N'short_code', N'medium',
 NULL,
 N'SELECT TOP 10 * FROM Customers ORDER BY CreatedAt DESC',
 N'TOP N + ORDER BY DESC ile son N kayıt alınır.', 15),


-- ============================================================
-- ZOR SEVİYE (15 soru)
-- ============================================================

(N'Hiç sipariş vermemiş müşterileri bulan sorguyu yazın (LEFT JOIN ile):',
 N'short_code', N'hard',
 NULL,
 N'SELECT c.* FROM Customers c LEFT JOIN Orders o ON c.Id = o.CustomerId WHERE o.Id IS NULL',
 N'LEFT JOIN sonrası IS NULL ile sağ tabloda eşleşmeyen kayıtlar bulunur.', 25),

(N'Aşağıdaki sorgu ne yapar?\nSELECT p.Name FROM Products p WHERE NOT EXISTS (SELECT 1 FROM OrderItems oi WHERE oi.ProductId = p.Id);',
 N'multiple_choice', N'hard',
 N'["Tüm ürünleri getirir", "Hiç sipariş edilmemiş ürünleri getirir", "En çok satılan ürünleri getirir", "Stoğu olan ürünleri getirir"]',
 N'1',
 N'NOT EXISTS — alt sorgu sonuç döndürmediğinde true olur, yani hiç sipariş edilmemiş ürünler.', 25),

(N'CTE (Common Table Expression) tanımlamak için hangi anahtar kelime?',
 N'multiple_choice', N'hard',
 N'["DECLARE", "WITH", "CREATE CTE", "DEFINE"]',
 N'1',
 N'WITH cte_adi AS (SELECT ...) SELECT * FROM cte_adi şeklinde tanımlanır.', 20),

(N'Window function''da satırları gruplamak ve sıralamak için kullanılan ifade:',
 N'multiple_choice', N'hard',
 N'["GROUP BY ... HAVING", "OVER (PARTITION BY ... ORDER BY ...)", "ORDER BY ... LIMIT", "JOIN ... ON"]',
 N'1',
 N'OVER (PARTITION BY kolon ORDER BY kolon) — analytic fonksiyonlarda kullanılır.', 25),

(N'Her kategoride en pahalı ürünü bulan sorguyu yazın (window function ile, kolonlar: CategoryId, Name, Price):',
 N'short_code', N'hard',
 NULL,
 N'SELECT CategoryId, Name, Price FROM (SELECT CategoryId, Name, Price, ROW_NUMBER() OVER (PARTITION BY CategoryId ORDER BY Price DESC) AS rn FROM Products) t WHERE rn = 1',
 N'ROW_NUMBER() + PARTITION BY ile her grup içinde sıralama yapılır.', 30),

(N'Aşağıdaki ifadelerden hangisi transaction''ı geri alır?',
 N'multiple_choice', N'hard',
 N'["COMMIT", "ROLLBACK", "SAVEPOINT", "UNDO"]',
 N'1',
 N'BEGIN TRAN ... ROLLBACK işlemleri geri alır, COMMIT kalıcı yapar.', 20),

(N'Bir tabloya yeni kolon eklemek için kullanılan komut:',
 N'multiple_choice', N'hard',
 N'["ALTER TABLE ... ADD", "MODIFY TABLE", "UPDATE TABLE", "ADD COLUMN TO"]',
 N'0',
 N'ALTER TABLE tablo_adi ADD kolon_adi tip; şeklindedir.', 20),

(N'Index ne işe yarar?',
 N'multiple_choice', N'hard',
 N'["Veriyi şifreler", "Sorgu performansını artırır", "Tabloyu yedekler", "İlişkileri tanımlar"]',
 N'1',
 N'Index, WHERE/JOIN/ORDER BY''da kullanılan kolonlarda sorguyu hızlandırır.', 20),

(N'PIVOT operatörü ne için kullanılır?',
 N'multiple_choice', N'hard',
 N'["Satırları sütuna dönüştürmek", "Tabloyu döndürmek", "İki tabloyu birleştirmek", "Veri silmek"]',
 N'0',
 N'PIVOT — satır verilerini sütun başlığı yapar (çapraz tablo).', 25),

(N'Bir ürünün son satıldığı tarihi bulan sorguyu yazın (Products + OrderItems + Orders, ProductId = 1 için):',
 N'short_code', N'hard',
 NULL,
 N'SELECT TOP 1 o.CreatedAt FROM Orders o INNER JOIN OrderItems oi ON o.Id = oi.OrderId WHERE oi.ProductId = 1 ORDER BY o.CreatedAt DESC',
 N'Çoklu JOIN sonrası TOP 1 + ORDER BY DESC ile en yeni tarih alınır.', 25),

(N'Aşağıdaki sorgu ne yapar?\nWITH SatisliUrunler AS (SELECT DISTINCT ProductId FROM OrderItems) SELECT p.Name FROM Products p INNER JOIN SatisliUrunler s ON p.Id = s.ProductId;',
 N'multiple_choice', N'hard',
 N'["Tüm ürünleri getirir", "En az bir kez satılmış ürünleri getirir", "Stoğu olan ürünleri getirir", "Hiç satılmamış ürünleri getirir"]',
 N'1',
 N'CTE ile satılan ürün ID''leri ayıklanıyor, sonra Products ile JOIN ile satılmış ürünler geliyor.', 25),

(N'COALESCE fonksiyonu ne yapar?',
 N'multiple_choice', N'hard',
 N'["NULL olmayan ilk değeri döndürür", "İki sütunu birleştirir", "Stringe dönüştürür", "Sayıyı yuvarlar"]',
 N'0',
 N'COALESCE(a, b, c) — a NULL değilse a, yoksa b, o da NULL ise c döner.', 20),

(N'Bir müşterinin toplam harcamasını ve sipariş sayısını birlikte getiren sorguyu yazın (CustomerId = 1 için):',
 N'short_code', N'hard',
 NULL,
 N'SELECT COUNT(*) AS SiparisSayisi, SUM(TotalAmount) AS ToplamHarcama FROM Orders WHERE CustomerId = 1',
 N'Tek SELECT''te birden fazla aggregate fonksiyon kullanılabilir.', 20),

(N'Stored procedure tanımlamak için kullanılan anahtar kelime:',
 N'multiple_choice', N'hard',
 N'["CREATE FUNCTION", "CREATE PROCEDURE", "CREATE SP", "DEFINE PROCEDURE"]',
 N'1',
 N'CREATE PROCEDURE sp_adi AS BEGIN ... END şeklinde tanımlanır.', 20),

(N'Aşağıdaki transaction''da bir hata olursa hangi komutla geri alınır?\nBEGIN TRAN;\n  UPDATE Products SET Stock = Stock - 1 WHERE Id = 1;\n  INSERT INTO OrderItems VALUES (...);\nIF @@ERROR <> 0 ___;\nELSE COMMIT;',
 N'fill_in_blank', N'hard',
 NULL,
 N'ROLLBACK',
 N'@@ERROR son komutun hata kodunu döner. Hata varsa ROLLBACK ile değişiklikler geri alınır.', 25);

PRINT '';
PRINT 'SqlQuestions seed verisi yuklendi.';
SELECT Difficulty, COUNT(*) AS Adet FROM SqlQuestions GROUP BY Difficulty;
GO
