-- ============================================================
-- 09_seed_business_requests.sql
-- ErenShop bağlamında, iş analistinin karşılaşabileceği tarzda
-- 40 adet gerçekçi geliştirme talebi.
-- ============================================================

USE ErenShopDB;
GO

-- Önce mevcut talepleri temizle (tekrar çalıştırılabilir olsun diye)
IF EXISTS (SELECT 1 FROM BusinessRequests)
BEGIN
    -- Submission'ı olan talepleri silmek FK ihlali yapacağından, sadece submission yoksa temizle
    IF NOT EXISTS (SELECT 1 FROM RequestSubmissions)
    BEGIN
        DELETE FROM BusinessRequests;
        DBCC CHECKIDENT ('BusinessRequests', RESEED, 0);
        PRINT 'Mevcut BusinessRequests kayitlari temizlendi.';
    END
    ELSE
    BEGIN
        PRINT 'RequestSubmissions kayitlari mevcut, BusinessRequests temizlenmedi.';
        RETURN;
    END
END
GO

INSERT INTO BusinessRequests (Title, Description, Difficulty, ExpectedKeywords, ExpectedSections, MinTotalWords)
VALUES
-- ===== KOLAY =====
(N'Ürün Yorumları ve Puanlama Sistemi',
 N'Müşteriler satın aldıkları ürünlere 1-5 yıldız arası puan verebilmeli ve yorum yazabilmeli. Yorumlar ürün sayfasında listelenmeli. Sadece o ürünü satın almış ve siparişi "Paid" statüsündeki müşteriler yorum bırakabilir. Aynı müşteri aynı ürüne tek yorum yapabilir, fakat sonradan güncelleyebilir. Ortalama puan ürün kartında gösterilmeli.',
 N'easy',
 N'yorum,puan,yıldız,review,rating,müşteri,ürün,sipariş,paid,ortalama',
 N'amaç,kapsam,iş kuralları,akış,veri modeli,kabul kriterleri',
 350),

(N'Favori Ürünler Listesi',
 N'Giriş yapan müşteriler beğendikleri ürünleri favorilere ekleyebilmeli. Profil sayfasında "Favorilerim" sekmesi olacak. Favorideki ürünün fiyatı düşerse müşteriye email/uygulama içi bildirim gitmeli. Favorilerden ürün çıkarılabilmeli. Bir müşteri en fazla 100 favori ekleyebilir.',
 N'easy',
 N'favori,wishlist,müşteri,bildirim,fiyat düşüşü,email,limit',
 N'amaç,iş kuralları,veri modeli,akış,bildirim',
 300),

(N'Kupon Kodu Sistemi',
 N'Pazarlama ekibi kupon kodu oluşturabilmeli (örn: BAYRAM2026). Kupon yüzdelik (%10) veya sabit (50 TL) indirim olabilir. Geçerlilik tarihi, min sepet tutarı, kullanım limiti (kaç defa kullanılabilir) ve müşteri başına kullanım limiti tanımlanabilir. Sepet ekranında kullanıcı kod girip uygulayabilmeli. Aynı sepete birden fazla kupon uygulanamaz.',
 N'medium',
 N'kupon,indirim,yüzdelik,sabit,geçerlilik,limit,sepet,pazarlama',
 N'amaç,kapsam,iş kuralları,veri modeli,akış,kabul kriterleri,test senaryoları',
 400),

(N'Stok Uyarı Email Bildirimi',
 N'Bir ürünün stoğu belirlenen eşik değerin (varsayılan 10) altına düşerse stok yönetim ekibine otomatik email gönderilmeli. Eşik değer ürün bazında özelleştirilebilmeli. Aynı ürün için aynı gün içinde tek bildirim gönderilir. Email içinde ürün adı, mevcut stok, son 30 gün satış adedi olmalı.',
 N'easy',
 N'stok,eşik,uyarı,email,bildirim,otomatik,ürün',
 N'amaç,iş kuralları,akış,veri modeli',
 300),

(N'Adres Defteri',
 N'Müşteriler birden fazla teslimat adresi kaydedebilmeli. Her adresin bir adı olur (Ev, İş, Yazlık vb.). Bir adres varsayılan olarak işaretlenebilir. Sipariş sırasında müşteri kayıtlı adreslerden birini seçer veya yeni adres ekler. Bir müşteri en fazla 10 adres kaydedebilir.',
 N'easy',
 N'adres,teslimat,varsayılan,müşteri,sipariş,etiket',
 N'amaç,iş kuralları,veri modeli,akış',
 300),

(N'Sipariş İptal İşlemi',
 N'Müşteri "Pending" veya "Processing" statüsündeki siparişlerini iptal edebilmeli. "Shipped" sonrası iptal mümkün değil. İptal edilince stok geri yüklenir, ödeme yapıldıysa iade süreci başlatılır. Sipariş statüsü "Cancelled" olur. İptal nedeni opsiyonel olarak alınabilir.',
 N'medium',
 N'iptal,sipariş,statü,stok,iade,ödeme,neden',
 N'amaç,iş kuralları,akış,kabul kriterleri,test senaryoları',
 400),

(N'Ödeme Yöntemi Olarak Havale/EFT',
 N'CreditCard dışında BankTransfer (havale/EFT) ödeme seçeneği eklenmeli. Müşteri havaleyi seçerse sipariş "PendingPayment" statüsüne geçer. 3 iş günü içinde ödeme görülmezse sipariş otomatik iptal olur, stok iade edilir. Muhasebe ekibi havale onaylandığında manuel olarak siparişi "Paid" yapar.',
 N'medium',
 N'havale,EFT,ödeme,statü,iptal,muhasebe,manuel onay',
 N'amaç,iş kuralları,akış,statü diyagramı,kabul kriterleri',
 400),

(N'Ürün Görseli Yükleme',
 N'Admin panelinden bir ürüne birden fazla görsel yüklenebilmeli (en fazla 5). Görsellerden biri kapak görseli olur. Görseller jpg/png/webp olabilir, max 2MB. Yüklenen görseller otomatik 800x800 ve 200x200 olarak resize edilir. Ürün listesinde kapak görseli görünür.',
 N'medium',
 N'görsel,resim,upload,kapak,resize,format,limit',
 N'amaç,iş kuralları,veri modeli,akış',
 350),

(N'Kategori Hiyerarşisi (Alt Kategoriler)',
 N'Mevcut kategorilere alt kategori desteği eklenmeli. Örn: "Elektronik" altında "Telefon", "Bilgisayar". 2 seviye derinlik yeterli. Ürün eklerken alt kategori seçilir. Üst kategori filtrelenince tüm alt kategorilerin ürünleri gösterilir. Alt kategorisi olan üst kategori silinemez.',
 N'medium',
 N'hiyerarşi,alt kategori,parent,seviye,filtre',
 N'amaç,iş kuralları,veri modeli,akış',
 350),

(N'Müşteri Şifre Sıfırlama',
 N'Müşteri şifresini unuttuğunda email adresini girip sıfırlama bağlantısı alabilmeli. Bağlantı 1 saat geçerli olmalı, tek kullanımlık. Yeni şifre min 8 karakter, 1 büyük harf ve 1 rakam içermeli. Şifre sıfırlama denemesi 1 saatte 3 ile sınırlı.',
 N'easy',
 N'şifre,sıfırlama,email,token,geçerlilik,güvenlik,deneme limiti',
 N'amaç,iş kuralları,akış,güvenlik,test senaryoları',
 350),

-- ===== ORTA =====
(N'Çoklu Para Birimi Desteği',
 N'Sistem TL dışında USD ve EUR ile de ürün fiyatlarını göstermeli. Kullanıcı arayüzün üst kısmından para birimini seçer. Kur bilgisi günlük olarak Merkez Bankası servisinden çekilir. Sipariş kayıt anındaki kur ile sabitlenir. Raporlar her zaman TL bazında saklanır.',
 N'medium',
 N'döviz,para birimi,kur,USD,EUR,TL,merkez bankası,sabitleme',
 N'amaç,kapsam,iş kuralları,entegrasyon,veri modeli,kabul kriterleri',
 450),

(N'Sipariş Takip ve Kargo Entegrasyonu',
 N'Sipariş "Shipped" olduğunda müşteriye kargo takip numarası verilmeli. Müşteri sipariş detayında "Kargoyu Takip Et" linkine tıklayınca kargo firmasının sitesine yönlendirilir. Kargo statüleri (Hazırlanıyor, Yolda, Dağıtımda, Teslim Edildi) sistemde de güncellenmeli. Teslim edildiğinde sipariş otomatik "Delivered" olur.',
 N'medium',
 N'kargo,takip,entegrasyon,statü,teslimat,otomatik güncelleme',
 N'amaç,entegrasyon,iş kuralları,statü diyagramı,akış',
 450),

(N'Müşteri Sadakat Puanı Sistemi',
 N'Her tamamlanan siparişte müşteri, sipariş tutarının %2''si kadar puan kazanır. 1 puan = 1 TL. Puanlar bir sonraki siparişte kullanılabilir, max sepet tutarının %50''si. Puanlar 1 yıl geçerli. İade edilen siparişin puanları geri alınır.',
 N'medium',
 N'sadakat,puan,kazanım,kullanım,geçerlilik,iade',
 N'amaç,iş kuralları,veri modeli,akış,test senaryoları',
 450),

(N'Sepet Hatırlatma E-postası',
 N'Sepetinde ürün olup 24 saat içinde sipariş vermeyen müşterilere hatırlatma maili gönderilir. Mail sepetteki ürünleri ve toplam tutarı içerir. Müşteri 3 gün sonra hala sipariş vermediyse ikinci bir mail gönderilir, bu maile %5 indirim kuponu eklenir. Daha fazla mail gönderilmez.',
 N'medium',
 N'sepet,hatırlatma,email,kupon,otomasyon,zamanlama',
 N'amaç,iş kuralları,akış,zamanlama,test senaryoları',
 400),

(N'Toplu Ürün İçe Aktarma (Excel)',
 N'Admin paneline Excel/CSV yükleyerek toplu ürün ekleme özelliği. Şablon dosyası indirilebilir. Yüklenen dosyada zorunlu kolonlar: name, category_id, price, stock. Hatalı satırlar atlanır, hata raporu gösterilir. Maksimum 1000 satır işlenir. Aynı isimli ürün varsa güncellenir mi yoksa atlanır mı seçilebilir.',
 N'medium',
 N'excel,csv,toplu,import,şablon,hata raporu,limit,güncelleme',
 N'amaç,iş kuralları,akış,doğrulama,kabul kriterleri',
 450),

(N'Ürün Karşılaştırma',
 N'Müşteri max 3 ürünü "Karşılaştır" listesine ekleyebilmeli. Karşılaştırma sayfasında özellikler (fiyat, stok, kategori, açıklama) yan yana gösterilir. Sadece aynı kategorideki ürünler karşılaştırılabilir. Liste tarayıcı oturumu boyunca tutulur.',
 N'easy',
 N'karşılaştırma,ürün,kategori,özellik,liste,oturum',
 N'amaç,iş kuralları,akış,kabul kriterleri',
 350),

(N'Sipariş Notu',
 N'Müşteri sipariş verirken not yazabilmeli (örn: "Kapıyı çalmayın, zile basın"). Not 500 karakteri geçemez. Sipariş detayında ve kargo etiketinde not görünmeli. Admin not değişikliği yapamaz, sadece görüntüler.',
 N'easy',
 N'sipariş notu,karakter limiti,kargo,görüntüleme',
 N'amaç,iş kuralları,veri modeli',
 250),

(N'Stoğu Olmayan Ürünleri Bildir',
 N'Stoğu biten bir üründe müşteri "Stoğa gelince haber ver" butonuna tıklayabilmeli. Email adresi alınır (giriş yaptıysa otomatik). Stok > 0 olduğunda kayıtlı kullanıcılara mail gönderilir. Bir email aynı ürün için tek defa kayıtlanır.',
 N'medium',
 N'stok,bildirim,email,bekleme listesi,otomatik',
 N'amaç,iş kuralları,akış,veri modeli',
 350),

(N'Admin Paneli — Sipariş Statü Yönetimi',
 N'Admin sipariş statüsünü manuel değiştirebilmeli. Geçerli geçişler: Pending→Processing, Processing→Shipped, Shipped→Delivered, herhangi bir statü→Cancelled. Her statü değişikliğinde sebep girilebilir. Müşteriye otomatik mail gönderilir. Tüm değişiklikler log''lanır.',
 N'medium',
 N'admin,statü,geçiş,log,mail,manuel,sebep',
 N'amaç,iş kuralları,statü diyagramı,akış,güvenlik',
 400),

(N'Müşteri Segmentasyonu',
 N'Müşteriler harcama miktarına göre segmentlere ayrılır: Bronz (0-1000 TL), Gümüş (1001-5000), Altın (5001-15000), Platin (15000+). Toplam harcama son 12 ayda kabul edilir. Segmentlere göre özel indirim kuponları, kargo bedavası gibi avantajlar tanımlanabilir. Müşterinin segmentine göre profilde rozet görünür.',
 N'medium',
 N'segment,bronz,gümüş,altın,platin,harcama,avantaj,rozet',
 N'amaç,iş kuralları,veri modeli,akış,kabul kriterleri',
 450),

(N'Ürün Etiketleri (Tag)',
 N'Ürünlere kategori dışında etiketler eklenebilmeli (yeni, indirimde, çok satan, sınırlı stok vb.). Bir ürünün birden fazla etiketi olabilir. Müşteri etiketle filtreleyebilir. "Çok satan" etiketi sistem tarafından otomatik atanır (son 30 günde en az 50 satılan).',
 N'medium',
 N'etiket,tag,filtre,otomatik,çok satan,yeni,indirim',
 N'amaç,iş kuralları,veri modeli,akış',
 400),

(N'Sipariş PDF Faturası',
 N'"Paid" statüsündeki sipariş için PDF fatura oluşturulabilir. Faturada müşteri bilgileri, ürün satırları, KDV (%20), genel toplam yer alır. Fatura sipariş detay sayfasından indirilir. Aynı sipariş için aynı fatura numarası tekrar üretilir.',
 N'medium',
 N'fatura,pdf,KDV,sipariş,paid,müşteri,toplam',
 N'amaç,iş kuralları,veri modeli,akış,kabul kriterleri',
 400),

(N'Çoklu Dil Desteği (TR/EN)',
 N'Arayüz ve ürün bilgileri (ad, açıklama) Türkçe ve İngilizce olarak gösterilmeli. Üst menüde dil seçici. Dil seçimi tarayıcıya kaydedilir. Admin ürün eklerken iki dilde de bilgi girer. Sadece TR girilirse EN otomatik TR''den doldurulur ve "tercüme bekliyor" işaretlenir.',
 N'medium',
 N'çoklu dil,çeviri,TR,EN,arayüz,ürün,otomatik',
 N'amaç,kapsam,iş kuralları,veri modeli,akış',
 450),

(N'Gelişmiş Ürün Arama (Filtreleme)',
 N'Mevcut keyword aramaya ek olarak fiyat aralığı, kategori, etiket, stok durumu, puan filtreleri eklenmeli. Filtreler birleşik (AND) çalışır. URL''e filtreler yansır (paylaşılabilir link). Sonuçlar sayfalanmış olur (20''şer).',
 N'medium',
 N'arama,filtre,fiyat,kategori,etiket,sayfalama,URL',
 N'amaç,iş kuralları,akış,kabul kriterleri,test senaryoları',
 400),

(N'İade Talebi Yönetimi',
 N'"Delivered" siparişler için müşteri 14 gün içinde iade talebi açabilir. Talep nedeni (hasarlı, beklediğim gibi değil, yanlış ürün vs.) seçilir. Talep onaylanırsa kargo kodu üretilir, müşteri ürünü gönderir. Ürün geldiğinde admin onaylayınca ödeme iade edilir, stok güncellenir.',
 N'hard',
 N'iade,talep,sebep,kargo,onay,statü,ödeme iadesi,stok',
 N'amaç,kapsam,iş kuralları,statü diyagramı,akış,kabul kriterleri,test senaryoları',
 500),

(N'Müşteri Adına Sipariş Açma (Çağrı Merkezi)',
 N'Çağrı merkezi operatörü, müşteri adına telefonla sipariş alabilir. Operatör panelde müşteriyi arar, sepet hazırlar, sipariş oluşturur. Ödeme link''i SMS ile müşteriye gider, müşteri linki açıp ödeme yapar. Sipariş üzerinde "operatör adı" görünür. Operatör başkasının sipariş geçmişini düzenleyemez.',
 N'hard',
 N'çağrı merkezi,operatör,müşteri adına,SMS,ödeme linki,yetki,güvenlik',
 N'amaç,kapsam,iş kuralları,güvenlik,akış,kabul kriterleri',
 500),

(N'Excel Rapor Dışa Aktarma',
 N'Tüm rapor sayfaları (günlük satış, ürün satışı, kategori, müşteri, düşük stok) Excel olarak dışa aktarılabilmeli. Tarih aralığı seçilir. Dosya adı: report_[tip]_[tarih].xlsx. 10.000 satırı geçen raporlar arka planda hazırlanır, hazır olunca mail ile bildirilir.',
 N'medium',
 N'excel,export,rapor,tarih aralığı,async,mail bildirim',
 N'amaç,iş kuralları,akış,performans',
 400),

(N'Kampanya Bannerları',
 N'Anasayfada üst kısımda kampanya bannerları gösterilir. Admin panelinden banner görseli, link, başlangıç ve bitiş tarihi tanımlanır. Aynı anda max 5 banner aktif olabilir. Banner''lar arasında 5 saniyede bir geçiş olur. Banner''a tıklanma sayısı izlenir.',
 N'easy',
 N'banner,kampanya,görsel,zamanlama,tıklama,analitik',
 N'amaç,iş kuralları,veri modeli,akış',
 350),

-- ===== ZOR =====
(N'B2B Müşteri Tipi ve Toptan Fiyatlandırma',
 N'Mevcut Customer modeline "müşteri tipi" alanı eklenir: B2C (bireysel) veya B2B (kurumsal). B2B müşteriler için vergi numarası, ünvan, fatura adresi zorunlu. Ürünler için B2C fiyatı ve B2B fiyatı ayrı tutulur. B2B müşteriler giriş yaptığında B2B fiyatları görür. B2B siparişlerde min sepet tutarı 1000 TL. Vade ödeme seçeneği (30/60 gün) B2B''ye özel.',
 N'hard',
 N'B2B,B2C,kurumsal,vergi numarası,toptan fiyat,vade,min sepet',
 N'amaç,kapsam,iş kuralları,veri modeli,akış,kabul kriterleri,test senaryoları',
 600),

(N'Çoklu Depo / Şube Stok Yönetimi',
 N'Sistemde birden fazla depo tanımlanabilir (örn: İstanbul, Ankara, İzmir). Her ürünün her depoda ayrı stoğu var. Sipariş verilirken müşterinin adresine en yakın depodan stok düşülür. Stok yoksa diğer depolardan kontrol edilir. Depolar arası transfer hareketi de loglanır. Raporlar depo bazında filtrelenir.',
 N'hard',
 N'depo,şube,stok,lokasyon,transfer,yakınlık,rapor',
 N'amaç,kapsam,iş kuralları,veri modeli,akış,test senaryoları',
 600),

(N'Abonelik (Subscription) Sipariş',
 N'Belirli ürünler (sarf malzemeleri vb.) abonelik olarak satın alınabilmeli. Müşteri 1 ay / 2 ay / 3 aylık tekrar sıklığı seçer. Belirlenen tarihte otomatik sipariş oluşur, ödeme kayıtlı karttan çekilir. Müşteri aboneliği iptal/duraklatabilir. Ödeme başarısız olursa 3 gün sonra yeniden denenir, hala başarısızsa abonelik askıya alınır.',
 N'hard',
 N'abonelik,subscription,tekrar,otomatik sipariş,iptal,duraklat,başarısız ödeme',
 N'amaç,kapsam,iş kuralları,veri modeli,statü diyagramı,akış,kabul kriterleri,test senaryoları',
 600),

(N'Hediye Çeki / Gift Card',
 N'Müşteri belirli tutarda hediye çeki satın alabilir. Çek alıcının email''ine gönderilir, üzerinde benzersiz kod olur. Alıcı kodu kullanarak sepete uygular. Çek tam veya kısmi kullanılabilir, kalan bakiye saklanır. Çek 1 yıl geçerli. Çekle yapılan ödeme nakit gibi muhasebede izlenir.',
 N'hard',
 N'hediye çeki,gift card,kod,bakiye,kısmi kullanım,geçerlilik,muhasebe',
 N'amaç,kapsam,iş kuralları,veri modeli,akış,kabul kriterleri,test senaryoları',
 600),

(N'Müşteri Yorumlarının Moderasyonu',
 N'Eklenen müşteri yorumları önce admin onayından geçer. Yasaklı kelime listesi (küfür vs.) varsa yorum otomatik "Spam" işaretlenir. Admin yorumu onaylar/reddeder. Reddedilen yorumlar müşteriye sebep ile bildirilir. Müşteri 1 hafta içinde 3 kez reddedilirse yorum yazma hakkı 30 gün kısıtlanır.',
 N'hard',
 N'moderasyon,yorum,onay,yasaklı kelime,spam,kısıtlama,bildirim',
 N'amaç,iş kuralları,akış,güvenlik,kabul kriterleri',
 500),

(N'Dinamik Fiyatlandırma Kuralları',
 N'Admin "Eğer X ise Y" formatında dinamik fiyat kuralları tanımlayabilir. Örnek: "Sepet tutarı > 500 TL ise kargo bedava", "Aynı kategoriden 3 ürün alınırsa %15 indirim", "Saat 22:00-08:00 arası tüm ürünler %5 indirimli". Kurallar öncelik sırasına göre uygulanır. Aynı sepete birden fazla kural uygulanabilir.',
 N'hard',
 N'dinamik fiyat,kural,koşul,kargo bedava,kategori indirimi,zaman bazlı,öncelik',
 N'amaç,kapsam,iş kuralları,veri modeli,akış,test senaryoları',
 600),

(N'Affiliate / Referans Sistemi',
 N'Her müşterinin benzersiz davet kodu olur. Yeni müşteri kayıt olurken kod girerse, hem davet eden hem yeni kayıt 50 TL kupon kazanır. Davet edilen kişi ilk alışverişini yaptıktan sonra kupon aktifleşir. Bir müşteri max 20 kişi davet edebilir.',
 N'hard',
 N'referans,davet,affiliate,kod,kupon,limit,aktivasyon',
 N'amaç,iş kuralları,veri modeli,akış,kabul kriterleri,test senaryoları',
 550),

(N'A/B Test Altyapısı',
 N'Pazarlama ekibi anasayfa banner''larını A/B test etmek istiyor. Sistem gelen müşterileri %50/%50 iki gruba ayırır, her grup farklı bannerı görür. Tıklama ve dönüşüm metrikleri grup bazında raporlanır. Aynı müşteri her zaman aynı grupta kalır. Birden fazla test paralel çalışabilir.',
 N'hard',
 N'A/B test,grup,banner,dönüşüm,metrik,paralel,oran',
 N'amaç,kapsam,iş kuralları,veri modeli,akış,raporlama',
 550),

(N'Çoklu Ödeme (Bölünmüş Ödeme)',
 N'Müşteri tek sipariş tutarını birden fazla ödeme yöntemiyle bölerek ödeyebilmeli. Örn: 500 TL''lik siparişin 200''ü kredi kartı, 200''ü hediye çeki, 100''ü puanla. Her ödeme ayrı kaydedilir. Herhangi biri başarısız olursa diğerleri de iptal edilir (atomik). Toplam tam tutara eşit olmalı.',
 N'hard',
 N'bölünmüş ödeme,multiple payment,atomik,kredi kartı,hediye çeki,puan',
 N'amaç,iş kuralları,akış,atomicity,kabul kriterleri,test senaryoları',
 600),

(N'Sepet Paylaşımı',
 N'Müşteri hazırladığı sepeti benzersiz link ile başkasıyla paylaşabilir. Karşı taraf linki açar, sepete bakar, kendi adına sipariş verir. Paylaşılan sepet 7 gün geçerli. Aynı kullanıcı 5''ten fazla aktif paylaşılmış sepete sahip olamaz. Stoğu biten ürünler işaretlenir.',
 N'medium',
 N'sepet paylaşımı,link,benzersiz,geçerlilik,limit,stok kontrolü',
 N'amaç,iş kuralları,akış,veri modeli,güvenlik',
 450),

(N'Canlı Sohbet (Live Chat) Modülü',
 N'Web sitesinde alt köşede canlı destek butonu olacak. Müşteri tıklayınca müsait destek temsilcisine yönlendirilir. Müsait temsilci yoksa offline form gösterilir. Mesajlar veritabanında saklanır, müşterinin sipariş ve müşteri bilgileri otomatik temsilciye gösterilir. Konuşma sonunda müşteri 1-5 yıldız değerlendirme verir.',
 N'hard',
 N'canlı sohbet,chat,temsilci,offline form,müşteri bilgi,değerlendirme',
 N'amaç,kapsam,iş kuralları,akış,entegrasyon,kabul kriterleri',
 550);

PRINT '';
PRINT 'BusinessRequests seed verisi yuklendi.';
SELECT Difficulty, COUNT(*) AS Adet FROM BusinessRequests GROUP BY Difficulty;
GO
