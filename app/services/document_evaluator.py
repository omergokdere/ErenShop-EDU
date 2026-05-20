"""
document_evaluator.py — Analiz Teknik Dokümanı kural tabanlı değerlendirici

LLM kullanılmaz. Tamamen deterministik kontroller:
  1) Strüktürel skor (0-100):
       - Her zorunlu bölümün başlığı dokümanda var mı?
       - O bölümün altındaki kelime sayısı min_words eşiğini geçiyor mu?
       - Placeholder metni hâlâ duruyor mu (silinmiş mi)?
  2) İçerik skoru (0-100):
       - Talebin beklenen anahtar kelimeleri (ExpectedKeywords) dokümanda geçiyor mu?
       - Toplam kelime sayısı talebin MinTotalWords değerini karşılıyor mu?

Sonuç: structural + content ortalaması.
"""
from io import BytesIO
import re
import json
from typing import Optional

from docx import Document

from app.services.document_template import TEMPLATE_SECTIONS


# Şablon yol gösterici (italik) metinler — değerlendirmede sayılmaması için
PLACEHOLDER_FRAGMENTS = [
    "buraya rastgele atanan",
    "köşeli parantez içindeki",
    "Bu bölüm opsiyoneldir",
    "Doküman Sonu",
]


def _normalize(text: str) -> str:
    """Türkçe karakter koruyarak küçük harfe çevirir, fazla boşlukları kırpar."""
    return re.sub(r"\s+", " ", (text or "")).strip().lower()


def _word_count(text: str) -> int:
    text = (text or "").strip()
    if not text:
        return 0
    return len(re.findall(r"\b[\wçğıöşüÇĞİÖŞÜ]+\b", text))


def _strip_section_number(title: str) -> str:
    """'3. Amaç ve Kapsam' → 'Amaç ve Kapsam' (numarayı kaldırır)"""
    return re.sub(r"^\s*\d+(\.\d+)*\.?\s*", "", title or "").strip()


def _extract_sections_from_docx(file_bytes: bytes) -> dict:
    """
    Docx dosyasını okuyup bölüm bazlı içerik döndürür.
    {section_key: "altındaki birleştirilmiş metin"} formatında.
    Bölüm başlıkları TEMPLATE_SECTIONS'tan tanınır.
    """
    doc = Document(BytesIO(file_bytes))

    # Başlık metnini key'e map'leyelim (numara olsun ya da olmasın eşleşsin)
    title_to_key = {}
    for s in TEMPLATE_SECTIONS:
        normalized_full = _normalize(s["title"])
        normalized_no_num = _normalize(_strip_section_number(s["title"]))
        title_to_key[normalized_full] = s["key"]
        title_to_key[normalized_no_num] = s["key"]

    # Tüm paragrafları sırayla gez, hangi bölümdeyiz takip et
    current_key: Optional[str] = None
    buckets = {s["key"]: [] for s in TEMPLATE_SECTIONS}
    buckets["__before__"] = []  # bölümlere girmeden önceki metinler (kapak vs.)

    for para in doc.paragraphs:
        text = (para.text or "").strip()
        if not text:
            continue

        normalized = _normalize(text)
        matched_key = title_to_key.get(normalized)

        # Bölüm başlığı olarak doğrudan eşleşmediyse, paragraf style'ı heading olabilir
        # ama yine de eşleştirmek için kontrol — başlık şablon kelimesi içeriyor mu
        if matched_key is None and para.style and "Heading" in (para.style.name or ""):
            for key_norm, k in title_to_key.items():
                if key_norm and key_norm in normalized:
                    matched_key = k
                    break

        if matched_key:
            current_key = matched_key
            continue

        # Placeholder fragmentleri at
        if any(_normalize(fr) in normalized for fr in PLACEHOLDER_FRAGMENTS):
            continue

        if current_key:
            buckets[current_key].append(text)
        else:
            buckets["__before__"].append(text)

    # Birleştir
    result = {key: "\n".join(parts).strip() for key, parts in buckets.items()}
    return result


def _content_is_placeholder_only(section_text: str, placeholder: str) -> bool:
    """
    Kullanıcı placeholder metni hiç silmemiş mi? Çok yüksek benzerlik varsa True.
    """
    if not section_text:
        return True
    if not placeholder:
        return False
    # Placeholder'daki tüm satırların büyük çoğunluğu metinde aynen geçiyorsa placeholder kalmış demektir
    placeholder_lines = [ln.strip() for ln in placeholder.split("\n") if ln.strip()]
    if not placeholder_lines:
        return False
    norm_text = _normalize(section_text)
    matched = sum(1 for ln in placeholder_lines if _normalize(ln) in norm_text)
    return matched / max(len(placeholder_lines), 1) > 0.7


def evaluate_document(file_bytes: bytes, business_request: dict) -> dict:
    """
    Bir dokümanın puanını döndürür. business_request:
      {
        'Title': str,
        'Description': str,
        'ExpectedKeywords': str (comma separated) | None,
        'ExpectedSections': str (comma separated) | None,
        'MinTotalWords': int
      }
    Dönüş: {
        'structural_score': float (0-100),
        'content_score': float (0-100),
        'total_score': float (0-100),
        'detail': dict (JSON saklanabilir)
    }
    """
    try:
        sections = _extract_sections_from_docx(file_bytes)
    except Exception as e:
        return {
            "structural_score": 0.0,
            "content_score": 0.0,
            "total_score": 0.0,
            "detail": {"error": f"Dokuman okunamadi: {str(e)}"},
        }

    # ============= STRÜKTÜREL DEĞERLENDİRME =============
    section_results = []
    structural_points = 0.0
    structural_max = 0.0

    for sec in TEMPLATE_SECTIONS:
        key = sec["key"]
        required = sec.get("required", True)
        min_words = sec.get("min_words", 20)
        # Zorunlu bölümler 2 puan, opsiyoneller 1 puan ağırlığında
        weight = 2.0 if required else 1.0
        structural_max += weight

        text = sections.get(key, "") or ""
        words = _word_count(text)
        is_placeholder = _content_is_placeholder_only(text, sec.get("placeholder", ""))

        # Skorlama:
        #   - Bölüm hiç yoksa: 0
        #   - Yalnız placeholder durmuş: 0.2 * weight (başlık var ama doldurulmamış)
        #   - Kelime sayısı min_words / 2 altında: 0.5 * weight
        #   - Kelime sayısı min_words altında ama min_words/2 üstünde: 0.75 * weight
        #   - Yeterli: weight
        if not text:
            earned = 0.0
            status = "missing"
        elif is_placeholder:
            earned = 0.2 * weight
            status = "placeholder_only"
        elif words >= min_words:
            earned = 1.0 * weight
            status = "ok"
        elif words >= min_words / 2:
            earned = 0.75 * weight
            status = "short"
        else:
            earned = 0.5 * weight
            status = "very_short"

        structural_points += earned
        section_results.append({
            "key": key,
            "title": sec["title"],
            "required": required,
            "min_words": min_words,
            "words": words,
            "status": status,
            "earned": round(earned, 2),
            "weight": weight,
        })

    structural_score = (structural_points / structural_max) * 100 if structural_max else 0

    # ============= İÇERİK DEĞERLENDİRME =============
    # Tüm metin tek havuz olarak
    full_text = "\n".join(sections.get(s["key"], "") for s in TEMPLATE_SECTIONS)
    full_text_norm = _normalize(full_text)
    total_words = _word_count(full_text)

    # Anahtar kelime taraması
    expected_keywords_raw = (business_request.get("ExpectedKeywords") or "").strip()
    keywords = [k.strip().lower() for k in re.split(r"[,;]", expected_keywords_raw) if k.strip()]
    keyword_results = []
    matched_count = 0
    for kw in keywords:
        if not kw:
            continue
        if kw in full_text_norm:
            matched_count += 1
            keyword_results.append({"keyword": kw, "found": True})
        else:
            keyword_results.append({"keyword": kw, "found": False})

    keyword_score = (matched_count / len(keywords) * 100) if keywords else 100.0

    # Min toplam kelime sayısı
    min_total = int(business_request.get("MinTotalWords") or 300)
    if total_words >= min_total:
        word_score = 100.0
    elif total_words >= min_total / 2:
        word_score = 60.0 + (total_words - min_total / 2) / (min_total / 2) * 40.0
    else:
        word_score = (total_words / (min_total / 2)) * 60.0

    word_score = max(0.0, min(100.0, word_score))

    # İçerik skoru = anahtar kelime %70 + kelime sayısı %30
    content_score = keyword_score * 0.7 + word_score * 0.3

    # ============= TOPLAM =============
    total_score = (structural_score + content_score) / 2.0

    detail = {
        "sections": section_results,
        "total_words": total_words,
        "min_total_words_required": min_total,
        "word_score": round(word_score, 2),
        "keywords": keyword_results,
        "keyword_score": round(keyword_score, 2),
        "structural_score": round(structural_score, 2),
        "content_score": round(content_score, 2),
    }

    return {
        "structural_score": round(structural_score, 2),
        "content_score": round(content_score, 2),
        "total_score": round(total_score, 2),
        "detail": detail,
    }
