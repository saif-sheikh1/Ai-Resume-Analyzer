# AI Resume Analyzer — API Documentation

Base URL: `http://localhost:8000/api`

Interactive API Docs (Swagger): `http://localhost:8000/docs`

---

## Authentication (`/api/auth`)

### Register
`POST /api/auth/register`
- **Request Body**:
```json
{
  "email": "user@example.com",
  "full_name": "John Doe",
  "password": "securepassword123"
}
```
- **Response** (`201 Created`):
```json
{
  "access_token": "eyJhbGci...",
  "refresh_token": "eyJhbGci...",
  "token_type": "bearer"
}
```

### Login
`POST /api/auth/login`
- **Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```
- **Response** (`200 OK`):
```json
{
  "access_token": "eyJhbGci...",
  "refresh_token": "eyJhbGci...",
  "token_type": "bearer"
}
```

### Refresh Token
`POST /api/auth/refresh`
- **Request Body**:
```json
{
  "refresh_token": "eyJhbGci..."
}
```

---

## User Profile (`/api/users`)

- `GET /api/users/me` — Get current user profile
- `PATCH /api/users/me` — Update user profile
- `POST /api/users/me/avatar` — Upload avatar image
- `POST /api/users/me/change-password` — Change password
- `DELETE /api/users/me` — Delete account

---

## Resumes (`/api/resumes`)

- `POST /api/resumes/upload` — Upload PDF/DOC/DOCX resume file
- `GET /api/resumes/` — List uploaded resumes
- `GET /api/resumes/{resume_id}` — Get single resume details
- `DELETE /api/resumes/{resume_id}` — Delete resume and file

---

## Analysis (`/api/analysis`)

- `POST /api/analysis/{resume_id}` — Run ATS scoring & Gemini AI analysis
- `GET /api/analysis/` — List all past analyses
- `GET /api/analysis/dashboard/stats` — Get aggregate stats for dashboard
- `GET /api/analysis/{analysis_id}` — Get detailed analysis result
- `DELETE /api/analysis/{analysis_id}` — Delete analysis

---

## Job Match & AI Features (`/api/job-match`)

- `POST /api/job-match/` — Compare resume against Job Description
- `GET /api/job-match/` — List job matches
- `GET /api/job-match/{match_id}` — Get single match details
- `POST /api/job-match/cover-letter` — Generate cover letter
- `POST /api/job-match/interview-prep` — Generate interview preparation Q&A

---

## Reports (`/api/reports`)

- `GET /api/reports/{analysis_id}/pdf` — Download PDF report binary
