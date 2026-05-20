"""
training_routes.py — Eğitim modülleri endpoint'leri
   /api/training/...
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Query
from fastapi.responses import StreamingResponse, FileResponse
from io import BytesIO

from app.schemas.training_schema import (
    ReviewSubmissionBody, StartSqlTestBody, SubmitAnswerBody, CompleteTestBody
)
from app.services import training_service
from app.services.document_template import build_template_docx, build_example_docx
from app.utils.response import success_response, error_response

router = APIRouter()


# ============================================================
# KULLANICILAR (basit)
# ============================================================
@router.get("/training/users")
def list_training_users():
    return success_response(data=training_service.list_users())


@router.get("/training/users/{user_id}")
def get_training_user(user_id: int):
    user = training_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail=error_response("Kullanici bulunamadi."))
    return success_response(data=user)


# ============================================================
# ANALİZ DOKÜMANI — TALEPLER
# ============================================================
@router.get("/training/requests/random")
def get_random_request(user_id: int = Query(..., description="Trainee user id")):
    """Kullanıcının daha önce onaylanmış cevabı olmayan rastgele bir geliştirme talebi döndürür."""
    req = training_service.get_random_request_for_user(user_id)
    if not req:
        raise HTTPException(
            status_code=404,
            detail=error_response("Bu kullanici tum talepleri tamamlamis veya aktif talep yok."),
        )
    return success_response(data=req)


@router.get("/training/requests")
def list_requests():
    return success_response(data=training_service.list_all_requests())


@router.get("/training/requests/{request_id}")
def get_request(request_id: int):
    req = training_service.get_request(request_id)
    if not req:
        raise HTTPException(status_code=404, detail=error_response("Talep bulunamadi."))
    return success_response(data=req)


# ============================================================
# ANALİZ DOKÜMANI — ŞABLON İNDİRME
# ============================================================
@router.get("/training/template")
def download_template(request_id: int = Query(None)):
    """
    Boş analiz teknik dokümanı şablonunu Word olarak indirir.
    request_id verilirse kapak sayfasına o talep yazılır.
    """
    title, desc = "", ""
    if request_id:
        req = training_service.get_request(request_id)
        if req:
            title = req.get("Title", "")
            desc = req.get("Description", "")

    docx_bytes = build_template_docx(title, desc)
    filename = "Analiz_Teknik_Dokumani_Sablonu.docx"
    if request_id:
        filename = f"Analiz_Sablonu_Talep_{request_id}.docx"

    return StreamingResponse(
        BytesIO(docx_bytes),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/training/template/example")
def download_example_template():
    """
    Tam doldurulmuş ÖRNEK analiz dokümanını indirir.
    Eren referans olarak kullanır; gerçek submission için boş şablonu doldurur.
    """
    docx_bytes = build_example_docx()
    return StreamingResponse(
        BytesIO(docx_bytes),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": 'attachment; filename="Ornek_Analiz_Dokumani_Favori_Listesi.docx"'},
    )


# ============================================================
# ANALİZ DOKÜMANI — SUBMISSION
# ============================================================
@router.post("/training/submissions", status_code=201)
async def upload_submission(
    user_id: int = Form(...),
    request_id: int = Form(...),
    file: UploadFile = File(...),
):
    """Doldurulmuş Word'ü yükle, otomatik değerlendir."""
    if not file.filename.lower().endswith(".docx"):
        raise HTTPException(status_code=400, detail=error_response("Sadece .docx dosyalari kabul edilir."))
    content = await file.read()
    submission, error = training_service.submit_document(user_id, request_id, file.filename, content)
    if error:
        raise HTTPException(status_code=400, detail=error_response(error))
    return success_response(message="Dokuman yuklendi ve degerlendirildi.", data=submission)


@router.get("/training/submissions/{submission_id}")
def get_submission(submission_id: int):
    sub = training_service.get_submission(submission_id)
    if not sub:
        raise HTTPException(status_code=404, detail=error_response("Submission bulunamadi."))
    return success_response(data=sub)


@router.get("/training/submissions/user/{user_id}")
def list_user_submissions(user_id: int):
    return success_response(data=training_service.list_submissions_for_user(user_id))


@router.get("/training/submissions")
def list_submissions(status: str = Query(None, description="pending|approved|rejected")):
    return success_response(data=training_service.list_all_submissions(status))


@router.put("/training/submissions/{submission_id}/review")
def review_submission(submission_id: int, body: ReviewSubmissionBody):
    """Admin onayı (approve / reject)"""
    sub, error = training_service.review_submission(submission_id, body.status, body.review_note)
    if error:
        raise HTTPException(status_code=400, detail=error_response(error))
    return success_response(message="Inceleme kaydedildi.", data=sub)


@router.get("/training/submissions/{submission_id}/download")
def download_submission_file(submission_id: int):
    """Yüklenmiş Word'ü indir (admin inceleme için)."""
    path = training_service.get_submission_file_path(submission_id)
    if not path:
        raise HTTPException(status_code=404, detail=error_response("Dosya bulunamadi."))
    import os
    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail=error_response("Dosya disk uzerinde bulunamadi."))
    return FileResponse(
        path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=os.path.basename(path),
    )


# ============================================================
# SQL TEST MODÜLÜ
# ============================================================
@router.post("/training/sql-tests/start", status_code=201)
def start_sql_test(body: StartSqlTestBody):
    test, error = training_service.start_test(body.user_id, body.easy_count, body.medium_count, body.hard_count)
    if error:
        raise HTTPException(status_code=400, detail=error_response(error))
    return success_response(message="Test baslatildi.", data=test)


@router.get("/training/sql-tests/{test_id}")
def get_sql_test(test_id: int):
    test = training_service.get_test(test_id)
    if not test:
        raise HTTPException(status_code=404, detail=error_response("Test bulunamadi."))
    return success_response(data=test)


@router.post("/training/sql-tests/answer")
def submit_sql_answer(body: SubmitAnswerBody):
    result, error = training_service.submit_answer(body.test_question_id, body.user_answer)
    if error:
        raise HTTPException(status_code=400, detail=error_response(error))
    return success_response(message="Cevap kaydedildi.", data=result)


@router.post("/training/sql-tests/{test_id}/complete")
def complete_sql_test(test_id: int):
    test, error = training_service.complete_test(test_id)
    if error:
        raise HTTPException(status_code=400, detail=error_response(error))
    return success_response(message="Test tamamlandi.", data=test)


@router.get("/training/sql-tests/user/{user_id}")
def list_user_sql_tests(user_id: int):
    return success_response(data=training_service.list_tests_for_user(user_id))
