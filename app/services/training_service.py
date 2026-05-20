"""
training_service.py — Eğitim modülleri iş mantığı
   1) Analiz teknik dokümanı egzersizi
   2) Dinamik SQL bilgi testi
"""
import os
import json
import re
from datetime import datetime
from typing import Optional

from app.database import get_connection
from app.utils.helpers import rows_to_list, row_to_dict
from app.services.document_evaluator import evaluate_document


# Yüklenen Word dosyalarının saklanacağı klasör (proje kökünde uploads/)
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ============================================================
# KULLANICI
# ============================================================
def get_user(user_id: int) -> Optional[dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT Id, FullName, Role, CreatedAt FROM TrainingUsers WHERE Id = ?", user_id)
    row = cur.fetchone()
    if not row:
        conn.close()
        return None
    result = row_to_dict(cur, row)
    conn.close()
    return result


def list_users() -> list:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT Id, FullName, Role, CreatedAt FROM TrainingUsers ORDER BY Id")
    result = rows_to_list(cur, cur.fetchall())
    conn.close()
    return result


# ============================================================
# ANALİZ DOKÜMANI MODÜLÜ
# ============================================================
def get_random_request_for_user(user_id: int) -> Optional[dict]:
    """
    Kullanıcıya henüz onaylı (approved) submission'ı olmayan rastgele bir aktif talep döner.
    Pending veya rejected submission'ı olan talepler tekrar gösterilebilir
    (Eren tekrar denesin diye) — ama approved olunca artık gelmez.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT TOP 1 *
        FROM BusinessRequests
        WHERE IsActive = 1
          AND Id NOT IN (
              SELECT RequestId FROM RequestSubmissions
              WHERE UserId = ? AND Status = 'approved'
          )
        ORDER BY NEWID()
        """,
        user_id,
    )
    row = cur.fetchone()
    if not row:
        conn.close()
        return None
    result = row_to_dict(cur, row)
    conn.close()
    return result


def get_request(request_id: int) -> Optional[dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM BusinessRequests WHERE Id = ?", request_id)
    row = cur.fetchone()
    if not row:
        conn.close()
        return None
    result = row_to_dict(cur, row)
    conn.close()
    return result


def list_all_requests() -> list:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM BusinessRequests ORDER BY Difficulty, Id")
    result = rows_to_list(cur, cur.fetchall())
    conn.close()
    return result


def submit_document(user_id: int, request_id: int, original_filename: str, file_bytes: bytes):
    """
    Word dokümanını kaydet ve değerlendir.
    Dönüş: (submission_dict, error)
    """
    user = get_user(user_id)
    if not user:
        return None, "Kullanici bulunamadi."

    req = get_request(request_id)
    if not req:
        return None, "Talep bulunamadi."

    # Dosyayı kaydet
    safe_name = re.sub(r"[^\w\.\-]+", "_", original_filename or "submission.docx")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    stored_name = f"u{user_id}_r{request_id}_{timestamp}_{safe_name}"
    stored_path = os.path.join(UPLOAD_DIR, stored_name)
    with open(stored_path, "wb") as f:
        f.write(file_bytes)

    # Değerlendir
    result = evaluate_document(file_bytes, req)

    # Kaydet
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO RequestSubmissions
          (UserId, RequestId, FileName, FilePath, StructuralScore, ContentScore, TotalScore, EvaluationDetail, Status, SubmittedAt)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pending', GETDATE())
        """,
        user_id,
        request_id,
        original_filename or stored_name,
        stored_path,
        result["structural_score"],
        result["content_score"],
        result["total_score"],
        json.dumps(result["detail"], ensure_ascii=False),
    )
    conn.commit()

    cur.execute("SELECT @@IDENTITY AS Id")
    new_id = int(cur.fetchone()[0])
    conn.close()

    return get_submission(new_id), None


def get_submission(submission_id: int) -> Optional[dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
          s.Id, s.UserId, s.RequestId, s.FileName, s.StructuralScore, s.ContentScore,
          s.TotalScore, s.EvaluationDetail, s.Status, s.ReviewNote, s.SubmittedAt, s.ReviewedAt,
          r.Title AS RequestTitle, r.Difficulty AS RequestDifficulty,
          u.FullName AS UserName
        FROM RequestSubmissions s
        INNER JOIN BusinessRequests r ON s.RequestId = r.Id
        INNER JOIN TrainingUsers u ON s.UserId = u.Id
        WHERE s.Id = ?
        """,
        submission_id,
    )
    row = cur.fetchone()
    if not row:
        conn.close()
        return None
    result = row_to_dict(cur, row)
    conn.close()
    # EvaluationDetail JSON parse
    if result.get("EvaluationDetail"):
        try:
            result["EvaluationDetail"] = json.loads(result["EvaluationDetail"])
        except Exception:
            pass
    return result


def list_submissions_for_user(user_id: int) -> list:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
          s.Id, s.UserId, s.RequestId, s.FileName, s.StructuralScore, s.ContentScore,
          s.TotalScore, s.Status, s.ReviewNote, s.SubmittedAt, s.ReviewedAt,
          r.Title AS RequestTitle, r.Difficulty AS RequestDifficulty
        FROM RequestSubmissions s
        INNER JOIN BusinessRequests r ON s.RequestId = r.Id
        WHERE s.UserId = ?
        ORDER BY s.SubmittedAt DESC
        """,
        user_id,
    )
    result = rows_to_list(cur, cur.fetchall())
    conn.close()
    return result


def list_all_submissions(status: Optional[str] = None) -> list:
    conn = get_connection()
    cur = conn.cursor()
    if status:
        cur.execute(
            """
            SELECT
              s.Id, s.UserId, s.RequestId, s.FileName, s.StructuralScore, s.ContentScore,
              s.TotalScore, s.Status, s.ReviewNote, s.SubmittedAt, s.ReviewedAt,
              r.Title AS RequestTitle, r.Difficulty AS RequestDifficulty,
              u.FullName AS UserName
            FROM RequestSubmissions s
            INNER JOIN BusinessRequests r ON s.RequestId = r.Id
            INNER JOIN TrainingUsers u ON s.UserId = u.Id
            WHERE s.Status = ?
            ORDER BY s.SubmittedAt DESC
            """,
            status,
        )
    else:
        cur.execute(
            """
            SELECT
              s.Id, s.UserId, s.RequestId, s.FileName, s.StructuralScore, s.ContentScore,
              s.TotalScore, s.Status, s.ReviewNote, s.SubmittedAt, s.ReviewedAt,
              r.Title AS RequestTitle, r.Difficulty AS RequestDifficulty,
              u.FullName AS UserName
            FROM RequestSubmissions s
            INNER JOIN BusinessRequests r ON s.RequestId = r.Id
            INNER JOIN TrainingUsers u ON s.UserId = u.Id
            ORDER BY s.SubmittedAt DESC
            """
        )
    result = rows_to_list(cur, cur.fetchall())
    conn.close()
    return result


def review_submission(submission_id: int, status: str, review_note: Optional[str]):
    if status not in ("approved", "rejected"):
        return None, "Gecersiz status. 'approved' veya 'rejected' olmali."
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT Id FROM RequestSubmissions WHERE Id = ?", submission_id)
    if not cur.fetchone():
        conn.close()
        return None, "Submission bulunamadi."
    cur.execute(
        """
        UPDATE RequestSubmissions
        SET Status = ?, ReviewNote = ?, ReviewedAt = GETDATE()
        WHERE Id = ?
        """,
        status, review_note, submission_id,
    )
    conn.commit()
    conn.close()
    return get_submission(submission_id), None


def get_submission_file_path(submission_id: int) -> Optional[str]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT FilePath FROM RequestSubmissions WHERE Id = ?", submission_id)
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None


# ============================================================
# SQL TEST MODÜLÜ
# ============================================================
def _pick_random_questions(difficulty: str, count: int) -> list:
    if count <= 0:
        return []
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT TOP (?) Id, QuestionText, QuestionType, Difficulty, OptionsJson, Points
        FROM SqlQuestions
        WHERE Difficulty = ? AND IsActive = 1
        ORDER BY NEWID()
        """,
        count, difficulty,
    )
    result = rows_to_list(cur, cur.fetchall())
    conn.close()
    return result


def start_test(user_id: int, easy: int, medium: int, hard: int):
    user = get_user(user_id)
    if not user:
        return None, "Kullanici bulunamadi."

    easy_qs = _pick_random_questions("easy", easy)
    medium_qs = _pick_random_questions("medium", medium)
    hard_qs = _pick_random_questions("hard", hard)
    all_qs = easy_qs + medium_qs + hard_qs

    if not all_qs:
        return None, "Soru havuzunda yeterli soru yok."

    total_points = sum(q["Points"] for q in all_qs)

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO SqlTests (UserId, TotalQuestions, TotalPoints, Status, StartedAt)
        VALUES (?, ?, ?, 'in_progress', GETDATE())
        """,
        user_id, len(all_qs), total_points,
    )
    conn.commit()
    cur.execute("SELECT @@IDENTITY AS Id")
    test_id = int(cur.fetchone()[0])

    # Soruları test'e bağla (sırayla)
    for order, q in enumerate(all_qs, start=1):
        cur.execute(
            """
            INSERT INTO SqlTestQuestions (TestId, QuestionId, QuestionOrder)
            VALUES (?, ?, ?)
            """,
            test_id, q["Id"], order,
        )
    conn.commit()
    conn.close()

    return get_test(test_id), None


def get_test(test_id: int) -> Optional[dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT t.*, u.FullName AS UserName
        FROM SqlTests t
        INNER JOIN TrainingUsers u ON t.UserId = u.Id
        WHERE t.Id = ?
        """,
        test_id,
    )
    row = cur.fetchone()
    if not row:
        conn.close()
        return None
    test = row_to_dict(cur, row)

    # Sorular ve cevaplar
    cur.execute(
        """
        SELECT
          tq.Id AS TestQuestionId, tq.QuestionOrder, tq.UserAnswer, tq.IsCorrect, tq.PointsEarned,
          q.Id AS QuestionId, q.QuestionText, q.QuestionType, q.Difficulty, q.OptionsJson, q.Points,
          q.Explanation, q.CorrectAnswer
        FROM SqlTestQuestions tq
        INNER JOIN SqlQuestions q ON tq.QuestionId = q.Id
        WHERE tq.TestId = ?
        ORDER BY tq.QuestionOrder
        """,
        test_id,
    )
    items = rows_to_list(cur, cur.fetchall())
    conn.close()

    # Test henüz bitmediyse Explanation ve doğru cevap gizlensin
    # (sadece tamamlanmış testlerde göster — aksi halde cevap sızar)
    if test["Status"] != "completed":
        for it in items:
            it.pop("Explanation", None)
            it.pop("CorrectAnswer", None)

    test["Questions"] = items
    return test


def _normalize_sql_answer(s: str) -> str:
    """SQL kodlarını normalize eder: küçük harf, fazla boşluk silinir, tırnak normalize."""
    if not s:
        return ""
    s = s.strip().lower()
    s = re.sub(r"\s+", " ", s)
    s = s.replace("''", "'")
    s = s.rstrip(";")
    return s


def _is_answer_correct(question_type: str, user_answer: str, correct_answer: str) -> bool:
    if user_answer is None:
        return False
    if question_type == "multiple_choice":
        return str(user_answer).strip() == str(correct_answer).strip()
    if question_type == "fill_in_blank":
        return _normalize_sql_answer(user_answer) == _normalize_sql_answer(correct_answer)
    if question_type == "short_code":
        return _normalize_sql_answer(user_answer) == _normalize_sql_answer(correct_answer)
    return False


def submit_answer(test_question_id: int, user_answer: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT tq.Id, tq.TestId, q.QuestionType, q.CorrectAnswer, q.Points, t.Status
        FROM SqlTestQuestions tq
        INNER JOIN SqlQuestions q ON tq.QuestionId = q.Id
        INNER JOIN SqlTests t ON tq.TestId = t.Id
        WHERE tq.Id = ?
        """,
        test_question_id,
    )
    row = cur.fetchone()
    if not row:
        conn.close()
        return None, "Test sorusu bulunamadi."
    _, test_id, qtype, correct, points, status = row

    if status == "completed":
        conn.close()
        return None, "Bu test zaten tamamlanmis."

    is_correct = _is_answer_correct(qtype, user_answer, correct)
    earned = points if is_correct else 0

    cur.execute(
        """
        UPDATE SqlTestQuestions
        SET UserAnswer = ?, IsCorrect = ?, PointsEarned = ?, AnsweredAt = GETDATE()
        WHERE Id = ?
        """,
        user_answer, 1 if is_correct else 0, earned, test_question_id,
    )
    conn.commit()
    conn.close()
    return {"test_question_id": test_question_id, "is_correct": is_correct, "points_earned": earned}, None


def complete_test(test_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT Id, Status, TotalPoints, TotalQuestions FROM SqlTests WHERE Id = ?", test_id)
    row = cur.fetchone()
    if not row:
        conn.close()
        return None, "Test bulunamadi."
    if row[1] == "completed":
        conn.close()
        return get_test(test_id), None

    total_points = row[2]
    total_questions = row[3]

    # Toplam ve doğru sayısı
    cur.execute(
        """
        SELECT
          COALESCE(SUM(PointsEarned), 0),
          COALESCE(SUM(CASE WHEN IsCorrect = 1 THEN 1 ELSE 0 END), 0)
        FROM SqlTestQuestions WHERE TestId = ?
        """,
        test_id,
    )
    earned_points, correct_count = cur.fetchone()
    earned_points = int(earned_points or 0)
    correct_count = int(correct_count or 0)
    score = (earned_points / total_points * 100) if total_points else 0

    cur.execute(
        """
        UPDATE SqlTests
        SET Status = 'completed', CompletedAt = GETDATE(),
            EarnedPoints = ?, CorrectCount = ?, Score = ?
        WHERE Id = ?
        """,
        earned_points, correct_count, round(score, 2), test_id,
    )
    conn.commit()
    conn.close()

    return get_test(test_id), None


def list_tests_for_user(user_id: int) -> list:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT Id, UserId, TotalQuestions, CorrectCount, TotalPoints, EarnedPoints,
               Score, Status, StartedAt, CompletedAt
        FROM SqlTests
        WHERE UserId = ?
        ORDER BY StartedAt DESC
        """,
        user_id,
    )
    result = rows_to_list(cur, cur.fetchall())
    conn.close()
    return result
