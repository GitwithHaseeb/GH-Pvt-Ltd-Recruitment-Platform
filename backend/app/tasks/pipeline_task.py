import structlog

from app.database import SessionLocal
from app.models import Candidate, EmailLog, JobPosition, RecruitmentCycle
from app.services.email_sender import send_offer_email
from app.tasks.celery_app import celery_app
from app.utils.offer_letter import generate_offer_letter

logger = structlog.get_logger()


@celery_app.task(name="app.tasks.pipeline_task.run_recruitment_pipeline_task")
def run_recruitment_pipeline_task() -> dict:
    from app.services.job_matcher import match_candidates_to_jobs

    db = SessionLocal()
    try:
        pending = db.query(Candidate).filter(Candidate.status == "pending").order_by(Candidate.ats_score.desc()).all()
        top_20 = pending[:20]
        positions = db.query(JobPosition).order_by(JobPosition.id.asc()).all()
        if len(top_20) < len(positions):
            return {"error": "Not enough candidates to run matching."}

        match = match_candidates_to_jobs(top_20, positions)
        selected_ids = set(match.mapping.values())

        for candidate in top_20:
            candidate.status = "selected" if candidate.id in selected_ids else "rejected"

        for role, candidate_id in match.mapping.items():
            candidate = db.get(Candidate, candidate_id)
            if not candidate:
                continue
            subject = f"Congratulations! You are appointed as {role} at GH Pvt Ltd"
            try:
                letter_path = generate_offer_letter(candidate.name, role)
                send_offer_email(candidate.email, candidate.name, role, letter_path)
                db.add(
                    EmailLog(
                        candidate_id=candidate.id,
                        recipient_email=candidate.email,
                        subject=subject,
                        status="sent",
                    )
                )
            except Exception as exc:  # noqa: BLE001
                db.add(
                    EmailLog(
                        candidate_id=candidate.id,
                        recipient_email=candidate.email,
                        subject=subject,
                        status="failed",
                        error_message=str(exc),
                    )
                )
                logger.error("offer_email_failed", candidate_id=candidate.id, error=str(exc))

        cycle = RecruitmentCycle(
            positions_matched=match.mapping,
            selected_candidate_ids=list(selected_ids),
        )
        db.add(cycle)
        db.commit()
        logger.info("pipeline_completed", selected_count=len(selected_ids))
        return match.mapping
    finally:
        db.close()
