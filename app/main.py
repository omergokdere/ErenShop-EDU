"""
main.py - FastAPI uygulamasının giriş noktası
Tüm route'lar buraya dahil edilir.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import json
import os

from app.config import APP_TITLE, APP_VERSION, APP_DESCRIPTION

# Tüm route modüllerini import ediyoruz
from app.routes import health_routes
from app.routes import category_routes
from app.routes import product_routes
from app.routes import customer_routes
from app.routes import cart_routes
from app.routes import order_routes
from app.routes import payment_routes
from app.routes import report_routes
from app.routes import training_routes

# FastAPI uygulamasını oluştur
# docs_url="/docs" → Swagger arayüzü adresi
# redoc_url="/redoc" → ReDoc arayüzü adresi
# Türkçe karakterlerin JSON'da bozulmaması için ensure_ascii=False
class UnicodeJSONResponse(JSONResponse):
    def render(self, content) -> bytes:
        return json.dumps(content, ensure_ascii=False).encode("utf-8")

app = FastAPI(
    title=APP_TITLE,
    version=APP_VERSION,
    description=APP_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
    default_response_class=UnicodeJSONResponse
)

# CORS ayarları - frontend veya Postman'dan istek atabilmek için
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Geliştirme ortamında herkese açık
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route'ları uygulamaya ekle
# prefix="/api" → tüm endpoint'ler /api ile başlar
app.include_router(health_routes.router, prefix="/api", tags=["Health"])
app.include_router(category_routes.router, prefix="/api", tags=["Categories"])
app.include_router(product_routes.router, prefix="/api", tags=["Products"])
app.include_router(customer_routes.router, prefix="/api", tags=["Customers"])
app.include_router(cart_routes.router, prefix="/api", tags=["Cart"])
app.include_router(order_routes.router, prefix="/api", tags=["Orders"])
app.include_router(payment_routes.router, prefix="/api", tags=["Payments"])
app.include_router(report_routes.router, prefix="/api", tags=["Reports"])
app.include_router(training_routes.router, prefix="/api", tags=["Training"])


@app.get("/", tags=["Root"])
def root():
    """Ana sayfa yönlendirmesi"""
    return {
        "message": "ErenShop API çalışıyor!",
        "docs": "/docs",
        "health": "/api/health",
        "frontend": "/frontend/index.html"
    }


# Frontend static dosyaları serve et
_frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')
if os.path.isdir(_frontend_path):
    app.mount("/frontend", StaticFiles(directory=_frontend_path, html=True), name="frontend")

# Docs klasörünü static olarak serve et (markdown dosyaları)
_docs_path = os.path.join(os.path.dirname(__file__), '..', 'docs')
if os.path.isdir(_docs_path):
    app.mount("/docs-files", StaticFiles(directory=_docs_path), name="docs-files")
