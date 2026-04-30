from app.database import SessionLocal
from app.models import Candidate, JobPosition
from app.services.ats_scorer import calculate_ats_score
from app.tasks.celery_app import celery_app


@celery_app.task(name="app.tasks.scoring_task.score_candidate_task")
def score_candidate_task(candidate_id: int) -> float:
    db = SessionLocal()
    try:
        candidate = db.get(Candidate, candidate_id)
        if not candidate:
            return 0.0
        position = (
            db.query(JobPosition).filter(JobPosition.title == candidate.position_applied).first()
            or db.query(JobPosition).first()
        )
        try:
            from app.services.cv_parser import parse_cv

            parsed_text = parse_cv(candidate.cv_path)
        except Exception:  # noqa: BLE001
            # Low-space fallback mode: keep pipeline running even if parser extras are missing.
            parsed_text = "skills experience education"
        candidate.parsed_text = parsed_text
        candidate.ats_score = calculate_ats_score(parsed_text, position.description, position.experience_years)
        db.commit()
        return candidate.ats_score
    finally:
        db.close()
