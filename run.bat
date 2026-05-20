@echo off
REM ============================================================
REM run.bat - ErenShop API'yi başlatır
REM Çalıştırmak için çift tıkla veya terminalde: .\run.bat
REM ============================================================

echo ErenShop API baslatiliyor...
echo Swagger: http://localhost:8000/docs
echo Durdurmak icin: CTRL+C
echo.

REM Sanal ortam aktifse onu kullan, değilse direkt çalıştır
IF EXIST "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
