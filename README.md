# GH Pvt Ltd – AI/ML Recruitment Platform

A complete software house website plus an intelligent recruitment pipeline with ATS scoring, embedding-based job matching, and automated offer emails.

**Company:** GH Pvt Ltd  
**CEOs:** Ghania Tanveer & Muhammad Haseeb  
**Domain:** Production-grade AI/ML Python delivery for US/UAE clients.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Quick Start (Local)](#quick-start-local)
- [Free Cloud Deployment (Student Path)](#free-cloud-deployment-student-path)
- [Live Deployment (What We Used)](#live-deployment-what-we-used)
- [Environment Variables](#environment-variables)
- [Gmail API Configuration (Email Import)](#gmail-api-configuration-email-import)
- [Admin Dashboard](#admin-dashboard)
- [Recruitment Pipeline Explained](#recruitment-pipeline-explained)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Features

### For visitors

- Modern software house website (Home, About, Services, Clients, Careers)
- Two apply options:
  - **Direct email** – opens **Gmail compose** in the browser with both CEO emails prefilled (subject/body template)
  - **Online form** – upload CV (PDF/DOCX), fill details, submit to backend

### For recruiters (automated)

- **Candidate ingestion** from:
  - Form submissions
  - Gmail inbox import (intended as a periodic worker task; see notes below)
- **ATS scoring** (deterministic 0–100 style hybrid scoring in code)
- **Job matching**:
  - Embedding similarity between CV text and job descriptions
  - Hard-skill overlap bonuses
  - **Hungarian assignment** to enforce **one candidate per role** (5 roles)
- **Automated offer emails**:
  - HTML email body
  - PDF offer letter attachment (generated)
  - SMTP retries in code paths that send mail

### Admin dashboard

- Total applicants (split by source when available)
- ATS distribution chart (frontend)
- Top candidates list (by ATS score)
- Selected candidates (post-pipeline)
- Pipeline trigger
- Email logs (when offers are sent)

---

## Tech Stack

| Layer | Technology |
| --- | --- |
| Frontend | Next.js 14 (App Router), TypeScript, TailwindCSS |
| Backend API | FastAPI |
| Database | PostgreSQL (SQLAlchemy ORM) |
| Queue (optional) | Redis + Celery (recommended for async tasks) |
| AI/ML | CV parsing (PDF/DOCX), embeddings + similarity, scipy assignment |
| Emails | SMTP (`smtplib`) + PDF generation (`reportlab`) |
| Local orchestration | Docker Compose (optional) |
| Free hosting path | Vercel (frontend) + Render (backend) + Neon (Postgres) + Upstash (Redis) |

---

## Project Structure

```text
GH-Pvt-Ltd-Recruitment-Platform/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI entry
│   │   ├── config.py               # settings
│   │   ├── models.py               # Candidate, JobPosition, EmailLog, RecruitmentCycle
│   │   ├── schemas.py              # Pydantic models
│   │   ├── api/                    # apply + admin routes
│   │   ├── services/               # parsers, ATS, matcher, email, gmail import
│   │   ├── tasks/                  # Celery tasks (optional runtime)
│   │   ├── rag/                    # embeddings + assignment helpers
│   │   └── utils/                  # uploads, offer letter, logging
│   ├── migrations/                 # Alembic (see migrations/README.md)
│   ├── seed_positions.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── app/                        # Next.js routes
│   ├── components/
│   ├── public/
│   ├── package.json
│   └── Dockerfile
├── docs/
│   ├── FREE_DEPLOYMENT_GUIDE.md    # step-by-step free deploy runbook
│   └── GH_Pvt_Ltd_Recruitment_Platform_IEEE_Style_Report.docx
├── scripts/
│   └── generate_ieee_style_report.py
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Quick Start (Local)

### Option A: Docker Compose (full stack)

**Prerequisites:** Docker Desktop + Docker Compose

1. Clone the repository:

```bash
git clone https://github.com/GitwithHaseeb/GH-Pvt-Ltd-Recruitment-Platform.git
cd GH-Pvt-Ltd-Recruitment-Platform
```

2. Configure environment:

```bash
cp .env.example .env
```

3. Start services:

```bash
docker compose up --build
```

4. Run migrations (if Alembic is configured for your environment):

```bash
docker compose exec backend alembic upgrade head
```

5. Seed 5 job positions:

```bash
docker compose exec backend python seed_positions.py
```

6. Open:

- Website: `http://localhost:3000`
- API docs: `http://localhost:8000/docs`
- Admin UI: `http://localhost:3000/admin`

### Option B: Local without Docker (student machines)

This repo supports a lightweight local mode, but production-like behavior (Celery schedules) still benefits from Redis + a worker process.

---

## Free Cloud Deployment (Student Path)

We documented the exact free-tier deployment flow here:

- `docs/FREE_DEPLOYMENT_GUIDE.md`

It covers:

- GitHub → Neon Postgres → Upstash Redis → Render (FastAPI) → Vercel (Next.js)
- Common build failures (Python version pinning, dependency issues)
- Vercel monorepo root directory pitfalls (`frontend/`)

---

## Live Deployment (What We Used)

### Live website (frontend)

- **Vercel (Hobby / free)**: [https://gh-pvt-ltd-recruitment-platform.vercel.app/](https://gh-pvt-ltd-recruitment-platform.vercel.app/)

This hosts the **Next.js** marketing site + apply/admin UI.

### Live API (backend)

- **Render (Web Service / free tier)**: `https://gh-backend-of1e.onrender.com`

This hosts the **FastAPI** API + recruitment endpoints.

Quick checks:

- Health: `https://gh-backend-of1e.onrender.com/health`
- Open roles: `https://gh-backend-of1e.onrender.com/api/positions`

### Platforms we used (and what each one does)

- **GitHub**: source control + automatic deploy hooks for Render/Vercel
- **Neon**: managed **PostgreSQL** database (`DATABASE_URL`)
- **Upstash**: managed **Redis** (`REDIS_URL` + Celery broker/result URLs)
- **Render**: hosts the **Python backend** (install deps, run `uvicorn`)
- **Vercel**: hosts the **Next.js frontend** and CDN-style delivery

### Frontend ↔ backend wiring

On Vercel, set:

- `NEXT_PUBLIC_API_BASE=https://gh-backend-of1e.onrender.com`

That value is what the browser uses to call the backend from the deployed website.

### Important free-tier notes (real world)

- **Render cold starts** on free web services can add ~30–90s latency after idle.
- **Render Background Workers** may be **paid** on some accounts/plans. For student demos, we added a **synchronous fallback** for `/api/run-pipeline` when workers are unavailable (tradeoff: long-running requests).

---

## Environment Variables

Copy `.env.example` to `.env` and fill values.

| Variable | Description |
| --- | --- |
| `DATABASE_URL` | Postgres connection string |
| `REDIS_URL` | Redis URL (Celery broker/backend if used) |
| `CELERY_BROKER_URL` | Celery broker URL |
| `CELERY_RESULT_BACKEND` | Celery result backend URL |
| `SMTP_HOST` / `SMTP_PORT` | SMTP server settings |
| `SMTP_USER` / `SMTP_PASS` | SMTP credentials (Gmail app password recommended) |
| `SMTP_FROM` | From header |
| `ADMIN_USERNAME` / `ADMIN_PASSWORD` | Admin basic auth |
| `NEXT_PUBLIC_API_BASE` | Public backend base URL for the frontend |

---

## Gmail API Configuration (Email Import)

Gmail import is optional but supported via OAuth credentials.

High-level steps:

1. Google Cloud Console → enable Gmail API
2. OAuth consent screen → create OAuth client (Desktop)
3. Download `credentials.json` into `backend/` (or mount securely in production)
4. Run OAuth bootstrap once to generate `token.json`

Project helper:

- `backend/setup_gmail_oauth.py`

Operational note:

- Reliable scheduled import typically requires **Celery beat** or an external cron. Render background workers may be paid depending on account/plan.

---

## Admin Dashboard

- URL (local): `http://localhost:3000/admin`
- Default credentials (change in env): `admin` / `admin123`

Admin API:

- `GET /api/admin/metrics` (HTTP Basic auth)
- `POST /api/run-pipeline` (HTTP Basic auth)

---

## Recruitment Pipeline Explained

### Phase 1: intake + ATS scoring

- CVs arrive via form upload (and optionally Gmail import)
- Parsed text feeds ATS scoring heuristics
- Score stored on candidate record

### Phase 2: gather top candidates

- Pipeline selects pending candidates sorted by ATS score
- Takes top 20 (requires enough pending candidates)

### Phase 3: embedding similarity + assignment

- Builds a candidate/job utility matrix
- Uses Hungarian assignment to pick **5 unique candidates** for **5 roles**

### Phase 4: offer emails

- Generates offer PDFs
- Sends SMTP HTML email
- Logs outcomes in `EmailLog`

Free-tier note:

- If Celery workers are not available, the API can execute the pipeline **synchronously** for demos (tradeoff: long request times).

---

## Testing

```bash
docker compose exec backend pytest -q
```

---

## Troubleshooting

| Problem | Likely fix |
| --- | --- |
| Render build fails on NLP/scientific wheels | Pin `PYTHON_VERSION` to a stable version (example: `3.11.9`) |
| `EmailStr` import error | Ensure `email-validator` is installed (`backend/requirements.txt`) |
| Vercel error about `public` output | Set Framework to **Next.js** and Root Directory to `frontend/` |
| Free Render cold start | First request after idle can take ~30–90s |
| Pipeline needs workers | Use Redis + Celery worker/beat, or rely on synchronous demo mode |

---

## License

Proprietary to GH Pvt Ltd unless otherwise stated.

---

## Acknowledgements

Built for GH Pvt Ltd leadership and engineering delivery standards.

---

## Technical report (IEEE-style)

A long-form Word report is included for academic submission style writeups:

- `docs/GH_Pvt_Ltd_Recruitment_Platform_IEEE_Style_Report.docx`

Regenerate (optional):

```bash
python scripts/generate_ieee_style_report.py
```
