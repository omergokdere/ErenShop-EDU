-- ============================================================
-- 08_training_tables.sql
-- Eğitim modülleri için tablolar:
--   1) Analiz teknik dokümanı egzersizi
--   2) Dinamik SQL bilgi testi
-- ============================================================

USE ErenShopDB;
GO

-- ============================================================
-- 1. TrainingUsers
-- Eğitim platformu kullanıcıları (Eren, vb.). Login kompleksitesi yok.
-- ============================================================
IF OBJECT_ID('TrainingUsers', 'U') IS NULL
BEGIN
    CREATE TABLE TrainingUsers (
        Id          INT IDENTITY(1,1) PRIMARY KEY,
        FullName    NVARCHAR(150)   NOT NULL,
        Role        NVARCHAR(50)    NOT NULL DEFAULT 'trainee',  -- trainee | admin
        CreatedAt   DATETIME        NOT NULL DEFAULT GETDATE()
    );
    PRINT 'TrainingUsers tablosu olusturuldu.';
END

-- ============================================================
-- 2. BusinessRequests
-- Eren'e rastgele atanacak geliştirme talebi havuzu.
-- ExpectedKeywords: değerlendirmede aranan terimler (virgülle ayrılmış).
-- ExpectedSections: hangi şablon bölümleri özellikle önemli (virgülle).
-- ============================================================
IF OBJECT_ID('BusinessRequests', 'U') IS NULL
BEGIN
    CREATE TABLE BusinessRequests (
        Id                  INT IDENTITY(1,1) PRIMARY KEY,
        Title               NVARCHAR(200)   NOT NULL,
        Description         NVARCHAR(MAX)   NOT NULL,
        Difficulty          NVARCHAR(20)    NOT NULL DEFAULT 'medium',  -- easy | medium | hard
        ExpectedKeywords    NVARCHAR(MAX)   NULL,
        ExpectedSections    NVARCHAR(MAX)   NULL,
        MinTotalWords       INT             NOT NULL DEFAULT 300,
        IsActive            BIT             NOT NULL DEFAULT 1,
        CreatedAt           DATETIME        NOT NULL DEFAULT GETDATE()
    );
    PRINT 'BusinessRequests tablosu olusturuldu.';
END

-- ============================================================
-- 3. RequestSubmissions
-- Eren'in doldurup yüklediği Word dokümanları ve değerlendirme sonuçları.
-- Bir kullanıcı bir talebi (approve edilmediği sürece) tekrar dolduramaz.
-- ============================================================
IF OBJECT_ID('RequestSubmissions', 'U') IS NULL
BEGIN
    CREATE TABLE RequestSubmissions (
        Id                  INT IDENTITY(1,1) PRIMARY KEY,
        UserId              INT             NOT NULL,
        RequestId           INT             NOT NULL,
        FileName            NVARCHAR(300)   NOT NULL,
        FilePath            NVARCHAR(500)   NOT NULL,
        StructuralScore     DECIMAL(5,2)    NOT NULL DEFAULT 0,  -- 0-100 başlık/zorunlu alan
        ContentScore        DECIMAL(5,2)    NOT NULL DEFAULT 0,  -- 0-100 kelime/keyword
        TotalScore          DECIMAL(5,2)    NOT NULL DEFAULT 0,  -- 0-100 ortalama
        EvaluationDetail    NVARCHAR(MAX)   NULL,                -- JSON: bölüm bazlı detay
        Status              NVARCHAR(20)    NOT NULL DEFAULT 'pending', -- pending | approved | rejected
        ReviewNote          NVARCHAR(MAX)   NULL,
        SubmittedAt         DATETIME        NOT NULL DEFAULT GETDATE(),
        ReviewedAt          DATETIME        NULL,

        CONSTRAINT FK_RequestSubmissions_User FOREIGN KEY (UserId)
            REFERENCES TrainingUsers(Id),
        CONSTRAINT FK_RequestSubmissions_Request FOREIGN KEY (RequestId)
            REFERENCES BusinessRequests(Id)
    );
    PRINT 'RequestSubmissions tablosu olusturuldu.';
END

-- ============================================================
-- 4. SqlQuestions
-- Dinamik SQL testi için soru bankası.
-- QuestionType: multiple_choice | fill_in_blank | short_code
-- OptionsJson: çoktan seçmeli sorular için ['A şıkkı', 'B şıkkı', ...] formatında
-- CorrectAnswer: çoktan seçmelide şık indeksi (0-based), fill_in_blank ve short_code'da düz metin
-- ============================================================
IF OBJECT_ID('SqlQuestions', 'U') IS NULL
BEGIN
    CREATE TABLE SqlQuestions (
        Id              INT IDENTITY(1,1) PRIMARY KEY,
        QuestionText    NVARCHAR(MAX)   NOT NULL,
        QuestionType    NVARCHAR(30)    NOT NULL,
        Difficulty      NVARCHAR(20)    NOT NULL,  -- easy | medium | hard
        OptionsJson     NVARCHAR(MAX)   NULL,
        CorrectAnswer   NVARCHAR(MAX)   NOT NULL,
        Explanation     NVARCHAR(MAX)   NULL,
        Points          INT             NOT NULL DEFAULT 10,
        IsActive        BIT             NOT NULL DEFAULT 1,
        CreatedAt       DATETIME        NOT NULL DEFAULT GETDATE()
    );
    PRINT 'SqlQuestions tablosu olusturuldu.';
END

-- ============================================================
-- 5. SqlTests
-- Başlatılan / tamamlanan testler.
-- ============================================================
IF OBJECT_ID('SqlTests', 'U') IS NULL
BEGIN
    CREATE TABLE SqlTests (
        Id              INT IDENTITY(1,1) PRIMARY KEY,
        UserId          INT             NOT NULL,
        TotalQuestions  INT             NOT NULL,
        CorrectCount    INT             NOT NULL DEFAULT 0,
        TotalPoints     INT             NOT NULL DEFAULT 0,
        EarnedPoints    INT             NOT NULL DEFAULT 0,
        Score           DECIMAL(5,2)    NOT NULL DEFAULT 0,  -- 0-100
        Status          NVARCHAR(20)    NOT NULL DEFAULT 'in_progress', -- in_progress | completed
        StartedAt       DATETIME        NOT NULL DEFAULT GETDATE(),
        CompletedAt     DATETIME        NULL,

        CONSTRAINT FK_SqlTests_User FOREIGN KEY (UserId)
            REFERENCES TrainingUsers(Id)
    );
    PRINT 'SqlTests tablosu olusturuldu.';
END

-- ============================================================
-- 6. SqlTestQuestions
-- Bir testin sorularını ve verilen cevapları tutar.
-- ============================================================
IF OBJECT_ID('SqlTestQuestions', 'U') IS NULL
BEGIN
    CREATE TABLE SqlTestQuestions (
        Id              INT IDENTITY(1,1) PRIMARY KEY,
        TestId          INT             NOT NULL,
        QuestionId      INT             NOT NULL,
        QuestionOrder   INT             NOT NULL,
        UserAnswer      NVARCHAR(MAX)   NULL,
        IsCorrect       BIT             NULL,
        PointsEarned    INT             NOT NULL DEFAULT 0,
        AnsweredAt      DATETIME        NULL,

        CONSTRAINT FK_SqlTestQuestions_Test FOREIGN KEY (TestId)
            REFERENCES SqlTests(Id),
        CONSTRAINT FK_SqlTestQuestions_Question FOREIGN KEY (QuestionId)
            REFERENCES SqlQuestions(Id)
    );
    PRINT 'SqlTestQuestions tablosu olusturuldu.';
END

PRINT '';
PRINT 'Tum training tablolari hazir.';
GO

-- ============================================================
-- Varsayılan kullanıcılar
-- ============================================================
IF NOT EXISTS (SELECT 1 FROM TrainingUsers WHERE FullName = 'Eren')
BEGIN
    INSERT INTO TrainingUsers (FullName, Role) VALUES ('Eren', 'trainee');
    PRINT 'Varsayilan trainee kullanici eklendi: Eren';
END

IF NOT EXISTS (SELECT 1 FROM TrainingUsers WHERE FullName = 'Omer')
BEGIN
    INSERT INTO TrainingUsers (FullName, Role) VALUES ('Omer', 'admin');
    PRINT 'Varsayilan admin kullanici eklendi: Omer';
END
GO
