from dataclasses import dataclass

from app.services.job_matcher import match_candidates_to_jobs


@dataclass
class C:
    id: int
    parsed_text: str


@dataclass
class P:
    id: int
    title: str
    description: str
    required_skills: dict
    experience_years: int


def test_matcher_returns_one_per_role():
    positions = [
        P(1, "Senior AI/ML Engineer", "deep learning nlp pytorch", {"keywords": ["pytorch", "nlp"]}, 5),
        P(2, "Junior Python Developer", "fastapi sqlalchemy python", {"keywords": ["fastapi", "sqlalchemy"]}, 1),
        P(3, "ML Ops Engineer", "mlops docker kubernetes", {"keywords": ["docker", "kubernetes"]}, 3),
        P(4, "Backend Engineer (Python)", "backend python postgresql redis", {"keywords": ["postgresql", "redis"]}, 3),
        P(5, "Data Scientist", "statistics pandas sklearn", {"keywords": ["pandas", "sklearn"]}, 2),
    ]
    candidates = [C(i, f"python experience {i} years fastapi docker pandas sklearn nlp pytorch") for i in range(1, 21)]
    result = match_candidates_to_jobs(candidates, positions)
    assert len(result.mapping) == 5
    assert len(set(result.mapping.values())) == 5
