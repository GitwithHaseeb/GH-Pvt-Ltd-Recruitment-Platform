from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Candidate, JobPosition
from app.schemas import CandidateRead, JobPositionRead
from app.tasks.scoring_task import score_candidate_task
from app.utils.file_storage import save_upload

router = APIRouter(prefix="/api", tags=["apply"])


@router.get("/positions", response_model=list[JobPositionRead])
def list_positions(db: Session = Depends(get_db)):
    return db.query(JobPosition).all()


@router.post("/apply/form", response_model=CandidateRead)
async def apply_form(
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(""),
    position_applied: str = Form(...),
    cover_letter: str = Form(""),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    try:
        cv_path = await save_upload(resume)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    candidate = Candidate(
        name=name,
        email=email,
        phone=phone,
        position_applied=position_applied,
        cv_path=cv_path,
        source="form",
        status="pending",
    )
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    try:
        score_candidate_task.delay(candidate.id)
    except Exception:  # noqa: BLE001
        # Local non-Docker fallback when Redis/Celery broker is unavailable.
        score_candidate_task(candidate.id)
    return candidate
