# AI Resume Analyzer & Job Match Platform

A full-stack production-ready SaaS application for AI-powered resume analysis, ATS scoring, job matching, cover letter generation, and interview preparation.

Built with **React 19**, **TypeScript**, **Vite**, **Tailwind CSS**, **FastAPI**, **SQLAlchemy**, **Alembic**, **Supabase (PostgreSQL & Storage)**, and **Google Gemini 1.5 Flash**.

---

## Features

- **JWT Authentication**: Secure Register, Login, Refresh Token, Logout with bcrypt password hashing and persistent sessions.
- **Landing Page**: Modern SaaS landing page with Hero, Features, Benefits, How It Works, Stats, Pricing, FAQ, and CTA sections.
- **Dashboard**: Real-time statistics, score history trends (Recharts), section score breakdowns, recent activity timeline, and quick actions.
- **Resume Upload & Parsing**: Drag-and-drop file upload (PDF, DOC, DOCX up to 10MB) with Supabase Storage integration and automated NLP extraction (PyMuPDF, pdfplumber, python-docx, spaCy).
- **ATS Scoring Engine**: 8-category weighted scoring algorithm (Contact Info, Formatting, Skills, Experience, Education, Keywords, Projects, Grammar) with missing keyword detection and actionable recommendations.
- **AI Resume Analysis**: Google Gemini 1.5 Flash integration generating executive summaries, top 5 strengths/weaknesses, formatting fixes, improved bullet points, and career advice.
- **Job Match**: Compare resumes against job descriptions with match percentage calculation, skill gap analysis, keyword matching, hiring probability indicator, and recommendations.
- **AI Cover Letter Generator**: Custom cover letters tailored by tone (Professional, Creative, Technical) based on resume and job description.
- **Interview Preparation**: HR, Technical, Behavioral (STAR format), and Coding questions with detailed sample answers.
- **History & PDF Reports**: Full analysis history with search, filter, delete, and server-side PDF report generation (ReportLab).
- **User Profile**: Edit profile, update full name, upload avatar to Supabase, and change passwords securely.
- **Dark & Light Mode**: Theme toggle with system preference detection and localStorage persistence.

---

## Tech Stack

### Frontend
- **Framework**: React 19 + TypeScript + Vite
- **Styling**: Tailwind CSS v4 + Vanilla CSS Design System
- **State Management**: Zustand
- **Data Fetching**: TanStack Query (React Query) + Axios
- **Animations**: Framer Motion
- **Charts**: Recharts
- **Icons**: Lucide React
- **Notifications**: Sonner

### Backend
- **Framework**: FastAPI (Python 3.12)
- **ORM & DB**: SQLAlchemy 2.0 + Alembic migrations
- **Database**: Supabase PostgreSQL
- **File Storage**: Supabase Storage
- **AI**: Google Gemini API (`google-generativeai`)
- **Parsing**: PyMuPDF, pdfplumber, python-docx, spaCy (`en_core_web_sm`)
- **PDF Generation**: ReportLab
- **Auth**: JWT (`python-jose`) + Passlib (bcrypt)
- **Rate Limiting**: Slowapi

---

## Project Structure

```
Ai Resume Analyzer/
├── backend/
│   ├── alembic/                 # Database migration scripts
│   ├── app/
│   │   ├── api/                 # FastAPI routes and dependencies
│   │   ├── core/                # Settings, security, logging
│   │   ├── db/                  # Engine, session, base model
│   │   ├── models/              # SQLAlchemy ORM models
│   │   ├── repositories/        # Data access layer
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── services/            # Business logic (ATS, AI, Storage, Parser, Reports)
│   │   └── main.py              # Application entry point
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/          # UI, Layout, Landing, Dashboard components
│   │   ├── hooks/               # Custom hooks
│   │   ├── lib/                 # API client & utilities
│   │   ├── pages/               # Route pages
│   │   ├── stores/              # Zustand state stores
│   │   ├── types/               # TypeScript type definitions
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.ts
│   ├── Dockerfile
│   └── .env.example
├── docker/
│   └── nginx.conf
├── docs/
│   ├── API.md
│   └── DEPLOYMENT.md
├── docker-compose.yml
├── .gitignore
├── .env.example
└── README.md
```

---

## Getting Started

### Prerequisites
- Node.js 20+
- Python 3.12+
- Supabase Project (PostgreSQL & Storage)
- Google Gemini API Key

### Environment Variables

Copy `.env.example` to `.env` in both `backend` and `frontend` directories:

```bash
# Backend (.env)
DATABASE_URL=postgresql://postgres:password@db.project.supabase.co:5432/postgres
SUPABASE_URL=https://project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
GEMINI_API_KEY=your-gemini-api-key
JWT_SECRET=your-jwt-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
FRONTEND_URL=http://localhost:5173
BACKEND_URL=http://localhost:8000

# Frontend (.env)
VITE_API_URL=http://localhost:8000
```

### Backend Setup

```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python -m spacy download en_core_web_sm
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

API Documentation will be available at `http://localhost:8000/docs`.

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The application will run at `http://localhost:5173`.

---

## Running with Docker Compose

```bash
docker-compose up --build
```

- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`

---

## License

MIT License
