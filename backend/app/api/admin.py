import secrets
import socket
from urllib.parse import urlparse

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import Candidate, EmailLog
from app.schemas import MetricsResponse, RunPipelineResponse
from app.tasks.pipeline_task import run_recruitment_pipeline_task

router = APIRouter(prefix="/api", tags=["admin"])
security = HTTPBasic()


def _is_redis_reachable(redis_url: str) -> bool:
    parsed = urlparse(redis_url)
    host = parsed.hostname or "localhost"
    port = parsed.port or 6379
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except OSError:
        return False


def admin_auth(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    user_ok = secrets.compare_digest(credentials.username, settings.admin_username)
    pass_ok = secrets.compare_digest(credentials.password, settings.admin_password)
    if not (user_ok and pass_ok):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return credentials.username


@router.post("/run-pipeline", response_model=RunPipelineResponse, dependencies=[Depends(admin_auth)])
def run_pipeline():
    # Free-tier fallback: if Redis/Celery is unavailable, execute pipeline synchronously.
    if not _is_redis_reachable(settings.redis_url):
        mapping = run_recruitment_pipeline_task()
        return RunPipelineResponse(message="Pipeline executed synchronously (no worker).", selected_mapping=mapping or {})
    try:
        async_result = run_recruitment_pipeline_task.delay()
        return RunPipelineResponse(message="Pipeline triggered.", selected_mapping={"task_id": async_result.id})
    except Exception:  # noqa: BLE001
        mapping = run_recruitment_pipeline_task()
        return RunPipelineResponse(message="Pipeline executed synchronously (worker fallback).", selected_mapping=mapping or {})


@router.get("/admin/metrics", response_model=MetricsResponse, dependencies=[Depends(admin_auth)])
def metrics(db: Session = Depends(get_db)):
    total = db.query(Candidate).count()
    split_raw = db.query(Candidate.source, func.count(Candidate.id)).group_by(Candidate.source).all()
    split = {k: v for k, v in split_raw}
    ats_distribution = [c.ats_score for c in db.query(Candidate).all()]
    top_candidates = db.query(Candidate).order_by(Candidate.ats_score.desc()).limit(20).all()
    selected = db.query(Candidate).filter(Candidate.status == "selected").all()
    logs = db.query(EmailLog).order_by(EmailLog.sent_at.desc()).limit(100).all()
    return MetricsResponse(
        total_candidates=total,
        source_split=split,
        ats_distribution=ats_distribution,
        top_candidates=top_candidates,
        selected_candidates=selected,
        email_logs=[
            {
                "candidate_id": x.candidate_id,
                "recipient_email": x.recipient_email,
                "subject": x.subject,
                "status": x.status,
                "sent_at": x.sent_at.isoformat(),
            }
            for x in logs
        ],
    )
