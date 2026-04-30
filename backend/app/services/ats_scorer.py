import re
from collections.abc import Iterable


def _tokenize(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-zA-Z][a-zA-Z0-9+#.-]*", text.lower()) if len(t) > 1}


def _jaccard(a: Iterable[str], b: Iterable[str]) -> float:
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 1.0
    union = sa | sb
    if not union:
        return 0.0
    return len(sa & sb) / len(union)


def _format_score(cv_text: str) -> float:
    cv = cv_text.lower()
    section_hits = sum(int(x in cv) for x in ("experience", "education", "skills"))
    section_score = section_hits / 3
    length_score = 1.0 if 200 <= len(cv_text) <= 12000 else 0.6
    value = 0.7 * section_score + 0.3 * length_score
    return float(max(0.0, min(1.0, value)))


def _experience_years(cv_text: str) -> float:
    matches = re.findall(r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years|yrs)", cv_text.lower())
    if not matches:
        return 0.0
    return max(float(m) for m in matches)


def calculate_ats_score(cv_text: str, job_description: str, required_experience: int) -> float:
    keyword_sim = _jaccard(_tokenize(cv_text), _tokenize(job_description))
    format_component = _format_score(cv_text)
    candidate_exp = _experience_years(cv_text)
    experience_component = min(candidate_exp / max(required_experience, 1), 1.0)
    score = (0.5 * keyword_sim + 0.2 * format_component + 0.3 * experience_component) * 100
    return round(float(score), 2)
