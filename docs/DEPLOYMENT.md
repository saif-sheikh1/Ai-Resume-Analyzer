# Deployment Guide — AI Resume Analyzer

This guide details deploying the application to production:
- **Frontend**: Vercel
- **Backend**: Render
- **Database & Storage**: Supabase

---

## 1. Supabase Setup

1. Create a project at [supabase.com](https://supabase.com).
2. Go to **Project Settings -> Database** and copy the Connection String (`postgresql://postgres:[password]@db.[ref].supabase.co:5432/postgres`).
3. Go to **Storage**, create a new bucket named `resumes` (Private or Public depending on requirements).
4. Run Alembic migrations from your local backend environment:
   ```bash
   alembic upgrade head
   ```

---

## 2. Backend Deployment (Render)

1. Connect your repository to [Render](https://render.com).
2. Create a new **Web Service**.
3. Select `Python 3` runtime or `Docker`.
4. Set Build Command:
   ```bash
   pip install -r requirements.txt && python -m spacy download en_core_web_sm && alembic upgrade head
   ```
5. Set Start Command:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
6. Add Environment Variables:
   - `DATABASE_URL`
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`
   - `SUPABASE_SERVICE_ROLE_KEY`
   - `GEMINI_API_KEY`
   - `JWT_SECRET`
   - `FRONTEND_URL` (URL of your Vercel deployment)

---

## 3. Frontend Deployment (Vercel)

1. Connect your repository to [Vercel](https://vercel.com).
2. Set Root Directory to `frontend`.
3. Build Command: `npm run build`
4. Output Directory: `dist`
5. Add Environment Variable:
   - `VITE_API_URL`: Your Render backend service URL (e.g. `https://ai-resume-analyzer-api.onrender.com`)

---

## 4. Docker Deployment (Alternative)

To deploy on a VPS (AWS EC2, DigitalOcean, Hetzner):

```bash
git clone <your-repo>
cd "Ai Resume Analyzer"
cp backend/.env.example backend/.env
# Fill in production secrets in backend/.env
docker-compose up -d --build
```
