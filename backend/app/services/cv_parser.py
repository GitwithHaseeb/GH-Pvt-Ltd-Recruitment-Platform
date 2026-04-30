import re
from pathlib import Path

import docx
import pdfplumber


def extract_text_from_pdf(path: str) -> str:
    text_parts: list[str] = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text_parts.append(page.extract_text() or "")
    return "\n".join(text_parts)


def extract_text_from_docx(path: str) -> str:
    document = docx.Document(path)
    return "\n".join(p.text for p in document.paragraphs)


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return re.sub(r"[^\w\s.,+-]", "", text).strip().lower()


def parse_cv(path: str) -> str:
    ext = Path(path).suffix.lower()
    if ext == ".pdf":
        return clean_text(extract_text_from_pdf(path))
    if ext == ".docx":
        return clean_text(extract_text_from_docx(path))
    raise ValueError("Unsupported CV format")
