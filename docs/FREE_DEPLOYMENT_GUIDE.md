# GH Pvt Ltd Recruitment Platform — Free Deployment Guide (Student Path)

This document captures the **exact end-to-end flow** we followed to take the project from local development to a **free-tier cloud deployment** (no paid domain required).

It is written as a practical runbook you can repeat on a fresh machine.

---

## 0) What you are deploying (two parts)

- **Frontend**: Next.js (App Router) in `frontend/`
- **Backend**: FastAPI in `backend/`

You will get two public URLs:
- Frontend (Vercel): `https://<your-vercel-app>.vercel.app`
- Backend (Render): `https://<your-render-service>.onrender.com`

---

## 1) Put the code on GitHub

From your project root:

```powershell
cd "d:\Projects\GH Pvt Ltd Recruitment Platform"
git status
git add .
git commit -m "chore: deployment-ready updates"
git push
```

If GitHub already has an initial commit and your local repo is unrelated, use:

```powershell
git pull origin main --allow-unrelated-histories
```

Resolve conflicts (if any), commit, then push.

---

## 2) Neon Postgres (free database)

1. Create Neon account (GitHub login recommended).
2. Create a project (pick nearest region, e.g. Singapore).
3. Enable **connection pooling** (recommended for serverless / hosted backends).
4. Copy the **pooled Postgres connection string**.

You will store it as:

- `DATABASE_URL`

---

## 3) Upstash Redis (free Redis)

1. Create Upstash Redis database.
2. Copy the **TCP URL** (starts with `rediss://`).

You will store it as:

- `REDIS_URL`
- `CELERY_BROKER_URL` (same value)
- `CELERY_RESULT_BACKEND` (same value)

Optional (REST API usage elsewhere):

- `UPSTASH_REDIS_REST_URL`
- `UPSTASH_REDIS_REST_TOKEN`

Security note:
- Treat Redis tokens like passwords. Rotate if exposed.

---

## 4) Render backend (free web service)

### 4.1 Create Web Service

1. Go to Render dashboard.
2. `New +` → `Web Service`
3. Connect GitHub repo.
4. Configure:
   - **Root Directory**: `backend`
   - **Runtime**: Python
   - **Build Command**:
     - `pip install --upgrade pip setuptools wheel && pip install -r requirements.txt`
   - **Start Command**:
     - `uvicorn app.main:app --host 0.0.0.0 --port 10000`

### 4.2 Environment variables (minimum)

Set these in Render → Service → **Environment**:

- `DATABASE_URL` (Neon pooled URL)
- `REDIS_URL` (Upstash TCP URL)
- `CELERY_BROKER_URL` (same as `REDIS_URL`)
- `CELERY_RESULT_BACKEND` (same as `REDIS_URL`)
- `ADMIN_USERNAME` / `ADMIN_PASSWORD`
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `SMTP_FROM`

Recommended for stable Python builds on Render:

- `PYTHON_VERSION` = `3.11.9`

### 4.3 Common Render build pitfalls (what we hit)

- **Python 3.14 default**: some scientific / NLP wheels may fail to compile.
  - Fix: set `PYTHON_VERSION=3.11.9`.
- **Missing `email-validator`**: Pydantic `EmailStr` requires it.
  - Fix: ensure `email-validator` is in `backend/requirements.txt`.

### 4.4 Verify backend is live

Open:

- `https://<render-service>.onrender.com/health`

Expected:

```json
{"status":"ok"}
```

Free tier cold start:
- First request after idle can take ~30–90 seconds.

---

## 5) Seed job positions (one-time)

Use Render Shell (or any shell with DB connectivity) from `backend/`:

```bash
python seed_positions.py
```

Verify:

- `GET https://<render-service>.onrender.com/api/positions`

---

## 6) Background workers on Render (paid on many accounts)

Render **Background Workers** may be **paid** depending on account/plan.

### Free workaround we implemented

- Admin endpoint `/api/run-pipeline` can execute **synchronously** when Celery/Redis worker path is unavailable.
- This supports demos and manual operations without paying for workers.

Tradeoffs:
- Long-running pipeline runs inside the web process (timeouts possible on very heavy workloads).
- Scheduled Gmail import still ideally needs a worker/cron.

---

## 7) Vercel frontend (free)

### 7.1 Create project

1. Vercel → New Project → import GitHub repo.
2. Set **Root Directory** to `frontend`.

### 7.2 Environment variable

Add:

- `NEXT_PUBLIC_API_BASE` = `https://<render-service>.onrender.com`

### 7.3 Framework settings (critical)

In Vercel project settings:

- **Framework Preset**: `Next.js`
- **Output Directory**: leave default (do not force `public`)
- **Root Directory**: `frontend` (not `./` at repo root)

### 7.4 Common Vercel error

If you see:

> No Output Directory named `public` found

It almost always means:
- Framework preset is not Next.js, OR
- Root directory is wrong (building repo root instead of `frontend/`).

Fix:
- Framework = Next.js
- Root Directory = `frontend`
- Redeploy with **Clear build cache**

---

## 8) End-to-end demo checklist

1. Open Vercel site `/apply?mode=form` and submit a test candidate.
2. Confirm backend DB row exists (optional): use admin metrics endpoint.
3. Open `/admin` and load metrics.
4. Trigger recruitment pipeline manually (free sync mode if workers unavailable).

---

## 9) Production hardening (next upgrades)

When budget allows:

- Paid worker for Celery + beat (reliable scheduling)
- Object storage for CVs (S3/R2)
- Secrets rotation + audit logs
- Rate limiting + abuse protection on public endpoints
- Monitoring (Sentry) + uptime checks

---

## 10) Support commands (local debugging)

Backend docs:

- `https://<render-service>.onrender.com/docs`

Common checks:

- `/health`
- `/api/positions`
- `/api/admin/metrics` (basic auth)
