# Deployment Guide — AI Resume Analyzer

This guide details deploying the application to production:
- **Frontend**: Vercel
- **Backend**: Render
- **Database & Storage**: Supabase

---

## 1. Vercel Deployment (Frontend)

We have configured **`vercel.json`** and monorepo root delegators so Vercel can deploy automatically regardless of your root directory setting.

### Option A: Import Whole Git Repository (Recommended)
1. Go to [Vercel Dashboard](https://vercel.com/dashboard) and click **Add New -> Project**.
2. Select your `Ai-Resume-Analyzer` GitHub repository.
3. Keep Root Directory as `./`.
4. Vercel will automatically detect `vite` framework, run `npm run build`, and use `frontend/dist`.
5. Under **Environment Variables**, add:
   - `VITE_API_URL`: `https://<your-render-backend-name>.onrender.com`
6. Click **Deploy**.

### Option B: Set Root Directory to `frontend`
1. Under Vercel Project Settings -> **General**, set **Root Directory** to `frontend`.
2. Framework Preset: **Vite**.
3. Environment Variables:
   - `VITE_API_URL`: `https://<your-render-backend-name>.onrender.com`
4. Click **Deploy**.

*Note: All page routes (`/dashboard`, `/upload`, `/analysis`, etc.) are configured with single-page application (SPA) rewrites to `/index.html` in `vercel.json`.*

---

## 2. Backend Deployment (Render)

1. Connect your repository to [Render](https://render.com).
2. Create a new **Web Service**.
3. Select `Python 3` runtime.
4. Set Root Directory to `backend`.
5. Build Command:
   ```bash
   pip install -r requirements.txt && python -m spacy download en_core_web_sm && alembic upgrade head
   ```
6. Start Command:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
7. Environment Variables:
   - `DATABASE_URL`: `postgresql://postgres:Airesume%40123@db.jzwuentvficzlzqsbtcv.supabase.co:5432/postgres`
   - `SUPABASE_URL`: `https://jzwuentvficzlzqsbtcv.supabase.co`
   - `SUPABASE_ANON_KEY`: `<your-supabase-anon-key>`
   - `SUPABASE_SERVICE_ROLE_KEY`: `<your-supabase-service-role-key>`
   - `GEMINI_API_KEY`: `<your-gemini-api-key>`
   - `JWT_SECRET`: `ai-resume-analyzer-jwt-secret-key-2026-production-secure`
   - `FRONTEND_URL`: `https://<your-vercel-app-name>.vercel.app`

---

## 3. Supabase Setup (Database & Storage)

1. Database is hosted at Supabase PostgreSQL: `db.jzwuentvficzlzqsbtcv.supabase.co`
2. Tables and indexes are generated via Alembic migration (`alembic upgrade head`).
3. Storage bucket `resumes` is auto-initialized on first file upload.

---

## 4. Local Docker Compose (Alternative)

```bash
docker-compose up -d --build
```
