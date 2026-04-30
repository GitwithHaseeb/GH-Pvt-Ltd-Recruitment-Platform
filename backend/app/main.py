from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.admin import router as admin_router
from app.api.apply import router as apply_router
from app.api.webhooks import router as webhooks_router
from app.config import settings
from app.database import Base, engine
from app.utils.file_storage import ensure_upload_dirs
from app.utils.logging_config import configure_logging

configure_logging()
app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(apply_router)
app.include_router(admin_router)
app.include_router(webhooks_router)


@app.on_event("startup")
def startup():
    ensure_upload_dirs()
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}
