# Free Deployment Guide (Student Friendly)

This project can be deployed without buying a domain.

## Recommended Free Stack
- Frontend: Vercel (free)
- Backend API + Worker: Render (free tier)
- Database: Neon Postgres (free)
- Redis: Upstash Redis (free)

## 1) Deploy Backend on Render
Create two Render services from the same repo:

1. **Web Service** (FastAPI)
   - Root directory: `backend`
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port 10000`

2. **Background Worker** (Celery worker)
   - Root directory: `backend`
   - Build command: `pip install -r requirements.txt`
   - Start command: `celery -A app.tasks.celery_app.celery_app worker -l info`

3. **Background Worker (Beat scheduler)**
   - Root directory: `backend`
   - Build command: `pip install -r requirements.txt`
   - Start command: `celery -A app.tasks.celery_app.celery_app beat -l info`

Set backend environment variables in Render:
- `DATABASE_URL` = your Neon connection string
- `REDIS_URL` = your Upstash redis URL
- `CELERY_BROKER_URL` = same as REDIS_URL
- `CELERY_RESULT_BACKEND` = same as REDIS_URL
- `ADMIN_USERNAME`, `ADMIN_PASSWORD`
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `SMTP_FROM`
- `GMAIL_API_CREDENTIALS_PATH`, `GMAIL_API_TOKEN_PATH` (or secure file storage approach)

## 2) Deploy Frontend on Vercel
Create a Vercel project from this repo:
- Root directory: `frontend`
- Framework: Next.js
- Env var:
  - `NEXT_PUBLIC_API_BASE` = your Render backend URL

After deploy, Vercel gives a public URL.

## 3) Database + Redis
- Neon: create free Postgres DB and copy URL
- Upstash: create free Redis and copy connection URL

## 4) Seed Jobs (one-time)
After backend deploy, run:
- Render Shell (or local against production DB):
  - `python seed_positions.py`

## 5) Gmail Auto-import (Email applicants)
The Gmail importer requires OAuth credentials/token accessible to your deployed backend.
Use secure persistent storage for these files, then run oauth bootstrap once:
- `python setup_gmail_oauth.py`

## 6) Important Runtime Notes
- If Redis/Celery is down, `/api/run-pipeline` returns `503` by design.
- This avoids hanging requests and clearly indicates worker unavailability.
- For public testing with friends, share your Vercel URL.

## 7) What your friends can test
- Apply form from website (stored in DB)
- Email compose path (Gmail direct compose)
- Admin metrics endpoint (with auth)
- Pipeline run (works once Redis + Celery workers are up)
