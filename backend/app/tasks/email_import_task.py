import re

from app.database import SessionLocal
from app.models import Candidate
from app.services.gmail_importer import fetch_application_emails
from app.tasks.celery_app import celery_app
from app.tasks.scoring_task import score_candidate_task


def _extract_name_email(sender: str) -> tuple[str, str]:
    match = re.match(r"(.*)<(.*)>", sender)
    if match:
        return match.group(1).strip().strip('"') or "Candidate", match.group(2).strip()
    return "Candidate", sender.strip()


@celery_app.task(name="app.tasks.email_import_task.import_emails_task")
def import_emails_task() -> int:
    db = SessionLocal()
    imported = 0
    try:
        emails = fetch_application_emails()
        for item in emails:
            if not item["cv_path"]:
                continue
            _, email = _extract_name_email(item["sender"])
            exists = db.query(Candidate).filter(Candidate.email == email, Candidate.cv_path == item["cv_path"]).first()
            if exists:
                continue
            name, email = _extract_name_email(item["sender"])
            candidate = Candidate(
                name=name,
                email=email,
                phone="",
                position_applied=item["position"],
                cv_path=item["cv_path"],
                source="email",
                status="pending",
            )
            db.add(candidate)
            db.commit()
            db.refresh(candidate)
            score_candidate_task.delay(candidate.id)
            imported += 1
        return imported
    finally:
        db.close()
