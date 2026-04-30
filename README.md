# GH Pvt Ltd Recruitment Platform

Production-ready AI/ML software house website + intelligent recruitment pipeline.

## Stack
- Frontend: Next.js 14, TypeScript, TailwindCSS
- Backend: FastAPI, PostgreSQL, Redis, Celery
- AI/ML: CV parser, ATS scoring, sentence-transformers RAG matching, Hungarian assignment
- Automation: Celery-driven offer email flow (n8n-style trigger->fetch->transform->send)

## Features
- Company website pages: Home, About, Services, Clients, Careers
- Apply flow with two options:
  - Direct email (`mailto`) to:
    - `ghaniatanveer061@gmail.com`
    - `haseebch8130@gmail.com`
  - Online form with CV upload (PDF/DOCX, max 5MB)
- Candidate ingestion from:
  - Form submissions
  - Gmail API polling every 5 minutes (subject contains `Application for`)
- ATS scoring (deterministic 0-100):
  - Keyword similarity (50%)
  - Resume formatting/length checks (20%)
  - Experience extraction + matching (30%)
- RAG job matching:
  - `all-MiniLM-L6-v2` embeddings
  - cosine similarity matrix
  - Hungarian optimization for unique assignment of 5 roles
- Automated offer emails with generated PDF offer letters
- Admin dashboard with metrics, ATS chart, top candidates, selected candidates, and pipeline trigger

## Project Structure
- `backend/` FastAPI app, services, tasks, tests
- `frontend/` Next.js app router UI
- `docker-compose.yml` local orchestration

## Setup
1. Clone and copy env:
   - `cp .env.example .env`
2. Start services:
   - `docker-compose up --build`
3. Run migrations (if Alembic configured):
   - `docker compose exec backend alembic upgrade head`
4. Seed 5 job positions:
   - `docker compose exec backend python seed_positions.py`
5. Open:
   - Website: `http://localhost:3000`
   - Backend docs: `http://localhost:8000/docs`
   - Admin page: `http://localhost:3000/admin`

## Gmail API Configuration
1. In Google Cloud Console:
   - Create project
   - Enable Gmail API
   - Configure OAuth consent screen
   - Create OAuth client credentials (Desktop app)
2. Save credentials file to:
   - `backend/credentials.json`
3. Run OAuth bootstrap once:
   - `docker compose exec backend python -c "from app.services.gmail_importer import setup_gmail_oauth; setup_gmail_oauth()"`
4. This generates:
   - `backend/token.json`
5. Celery beat imports candidate emails every 5 minutes.

## API Endpoints
- `POST /api/apply/form` submit form and CV
- `GET /api/positions` list open roles
- `POST /api/run-pipeline` run recruitment pipeline (admin auth)
- `GET /api/admin/metrics` admin dashboard data (admin auth)

## Admin Credentials
- Default: `admin / admin123`
- Configure with `.env`:
  - `ADMIN_USERNAME`
  - `ADMIN_PASSWORD`

## Tests
Run:
- `docker compose exec backend pytest -q`

Included tests verify:
- ATS scoring determinism
- One-candidate-per-role matching
- Offer email content correctness

## Notes
- The pipeline is idempotent for repeated runs with existing statuses.
- Email sending has retries.
- Structured JSON logging is enabled with `structlog`.
