"""
training_schema.py — Eğitim modülleri (analiz dokümanı + SQL test) Pydantic modelleri.
"""
from pydantic import BaseModel
from typing import Optional, List


# ============= Analiz dokümanı =============
class ReviewSubmissionBody(BaseModel):
    """Admin'in submission'ı onaylama/reddetme payload'u"""
    status: str  # 'approved' | 'rejected'
    review_note: Optional[str] = None


# ============= SQL Test =============
class StartSqlTestBody(BaseModel):
    """Yeni SQL testi başlatma"""
    user_id: int
    easy_count: int = 4
    medium_count: int = 4
    hard_count: int = 2


class SubmitAnswerBody(BaseModel):
    """Test sorusunun cevabını gönderme"""
    test_question_id: int
    user_answer: str


class CompleteTestBody(BaseModel):
    """Testi sonlandır — tüm cevaplar gönderildikten sonra çağrılır"""
    test_id: int
