from dataclasses import dataclass

import numpy as np

from app.models import Candidate, JobPosition
from app.rag.embedding import embed_texts
from app.rag.hungarian import solve_assignment


@dataclass
class MatchResult:
    mapping: dict[str, int]
    score_matrix: list[list[float]]


def _skills_bonus(cv_text: str, skills: list[str]) -> float:
    text = cv_text.lower()
    hits = sum(1 for s in skills if s.lower() in text)
    return hits / max(len(skills), 1)


def match_candidates_to_jobs(candidates: list[Candidate], positions: list[JobPosition]) -> MatchResult:
    if len(candidates) < len(positions):
        raise ValueError("Need at least as many candidates as positions.")

    cv_embeddings = embed_texts([c.parsed_text for c in candidates])
    job_embeddings = embed_texts([p.description for p in positions])
    matrix: list[list[float]] = []
    for job_idx, position in enumerate(positions):
        row: list[float] = []
        for cand_idx, candidate in enumerate(candidates):
            cosine = float(np.dot(job_embeddings[job_idx], cv_embeddings[cand_idx]))
            skill_bonus = _skills_bonus(candidate.parsed_text, position.required_skills.get("keywords", []))
            exp_bonus = min(
                max(_extract_exp(candidate.parsed_text), 0.0) / max(position.experience_years, 1),
                1.0,
            )
            row.append(0.7 * cosine + 0.2 * skill_bonus + 0.1 * exp_bonus)
        matrix.append(row)

    rows, cols = solve_assignment(matrix)
    mapping = {positions[r].title: candidates[c].id for r, c in zip(rows, cols)}
    return MatchResult(mapping=mapping, score_matrix=matrix)


def _extract_exp(text: str) -> float:
    import re

    matches = re.findall(r"(\d+(?:\.\d+)?)\s*(?:years|yrs)", text.lower())
    if not matches:
        return 0.0
    return max(float(m) for m in matches)
