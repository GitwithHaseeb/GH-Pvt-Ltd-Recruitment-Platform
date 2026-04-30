from datetime import datetime

from sqlalchemy import JSON, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=True)
    position_applied: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    cv_path: Mapped[str] = mapped_column(String(500), nullable=False)
    source: Mapped[str] = mapped_column(String(20), default="form", nullable=False)
    parsed_text: Mapped[str] = mapped_column(Text, default="", nullable=False)
    ats_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class JobPosition(Base):
    __tablename__ = "job_positions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    required_skills: Mapped[dict] = mapped_column(JSON, nullable=False)
    experience_years: Mapped[int] = mapped_column(Integer, nullable=False)
    education: Mapped[str] = mapped_column(String(255), nullable=False)


class RecruitmentCycle(Base):
    __tablename__ = "recruitment_cycles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    positions_matched: Mapped[dict] = mapped_column(JSON, nullable=False)
    selected_candidate_ids: Mapped[list] = mapped_column(JSON, nullable=False)
    completed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class EmailLog(Base):
    __tablename__ = "email_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    candidate_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    recipient_email: Mapped[str] = mapped_column(String(255), nullable=False)
    subject: Mapped[str] = mapped_column(String(500), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    error_message: Mapped[str] = mapped_column(Text, default="", nullable=False)
    sent_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
