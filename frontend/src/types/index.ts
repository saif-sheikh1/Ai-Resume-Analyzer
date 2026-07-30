/* ─── TypeScript types for the application ─── */

export interface User {
  id: string;
  email: string;
  full_name: string;
  avatar_url: string | null;
  preferences: Record<string, unknown> | null;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface Resume {
  id: string;
  user_id: string;
  filename: string;
  file_url: string;
  file_type: string;
  file_size: number;
  parsed_data: ParsedResumeData | null;
  raw_text: string | null;
  created_at: string;
}

export interface ParsedResumeData {
  name: string | null;
  email: string | null;
  phone: string | null;
  address: string | null;
  summary: string | null;
  skills: string[];
  experience: ExperienceEntry[];
  education: EducationEntry[];
  projects: ProjectEntry[];
  certifications: string[];
  languages: string[];
}

export interface ExperienceEntry {
  title?: string;
  dates?: string;
  description?: string[];
}

export interface EducationEntry {
  degree?: string;
  institution?: string;
  dates?: string;
  details?: string[];
}

export interface ProjectEntry {
  name?: string;
  description?: string[];
}

export interface Analysis {
  id: string;
  resume_id: string;
  user_id: string;
  ats_score: number | null;
  section_scores: Record<string, number> | null;
  ai_summary: string | null;
  strengths: string[] | null;
  weaknesses: string[] | null;
  suggestions: string[] | null;
  missing_skills: string[] | null;
  improved_bullets: string[] | null;
  career_advice: string | null;
  formatting_suggestions: string[] | null;
  grammar_improvements: string[] | null;
  created_at: string;
}

export interface AnalysisListItem {
  id: string;
  resume_id: string;
  ats_score: number | null;
  ai_summary: string | null;
  created_at: string;
  resume_filename: string | null;
}

export interface DashboardStats {
  total_resumes: number;
  total_analyses: number;
  average_ats_score: number;
  highest_ats_score: number;
  recent_analyses: AnalysisListItem[];
  score_history: ScoreHistoryEntry[];
}

export interface ScoreHistoryEntry {
  score: number;
  date: string;
  filename: string;
}

export interface JobMatch {
  id: string;
  resume_id: string;
  user_id: string;
  job_title: string | null;
  company_name: string | null;
  job_description: string;
  match_percentage: number | null;
  matching_skills: string[] | null;
  missing_skills: string[] | null;
  keyword_analysis: Record<string, unknown> | null;
  hiring_probability: string | null;
  recommendations: string[] | null;
  cover_letter: string | null;
  interview_questions: Record<string, unknown> | null;
  created_at: string;
}

export interface JobMatchListItem {
  id: string;
  resume_id: string;
  job_title: string | null;
  company_name: string | null;
  match_percentage: number | null;
  hiring_probability: string | null;
  created_at: string;
}

export interface CoverLetterResponse {
  cover_letter: string;
  job_match_id?: string;
}

export interface InterviewQuestion {
  question: string;
  sample_answer: string;
  difficulty: string;
  category?: string;
}

export interface InterviewPrepResponse {
  hr_questions: InterviewQuestion[];
  technical_questions: InterviewQuestion[];
  behavioral_questions: InterviewQuestion[];
  coding_questions: InterviewQuestion[];
  improvement_suggestions: string[];
}
