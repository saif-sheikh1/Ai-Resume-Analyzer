"""
Resume parser service — extracts structured data from PDF/DOCX resumes.
Uses PyMuPDF, pdfplumber, python-docx, spaCy, and regex.
"""
import re
from typing import Optional

from app.core.logging import get_logger

logger = get_logger(__name__)

# Try to load spaCy model
try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
    SPACY_AVAILABLE = True
except Exception:
    SPACY_AVAILABLE = False
    nlp = None
    logger.warning("spaCy model not available — NER extraction will be limited")


# ─── Skill Keywords Database ───────────────────────────────────────
TECHNICAL_SKILLS = {
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust", "ruby",
    "php", "swift", "kotlin", "scala", "r", "matlab", "perl", "sql", "nosql",
    "html", "css", "react", "angular", "vue", "svelte", "next.js", "node.js",
    "express", "django", "flask", "fastapi", "spring", "rails", ".net", "laravel",
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "jenkins", "ci/cd",
    "git", "linux", "rest", "graphql", "grpc", "microservices", "api",
    "machine learning", "deep learning", "nlp", "computer vision", "tensorflow",
    "pytorch", "scikit-learn", "pandas", "numpy", "data science", "data analysis",
    "data engineering", "etl", "spark", "hadoop", "kafka", "airflow",
    "postgresql", "mysql", "mongodb", "redis", "elasticsearch", "dynamodb",
    "firebase", "supabase", "prisma", "sqlalchemy",
    "figma", "sketch", "adobe xd", "photoshop", "illustrator",
    "agile", "scrum", "kanban", "jira", "confluence",
    "tailwind", "bootstrap", "sass", "less", "webpack", "vite",
    "testing", "jest", "pytest", "selenium", "cypress", "playwright",
    "mobile", "react native", "flutter", "ios", "android",
    "blockchain", "web3", "solidity", "smart contracts",
    "devops", "sre", "monitoring", "logging", "prometheus", "grafana",
}

SOFT_SKILLS = {
    "leadership", "communication", "teamwork", "problem solving", "critical thinking",
    "time management", "project management", "collaboration", "adaptability",
    "creativity", "analytical", "attention to detail", "organization",
    "presentation", "negotiation", "mentoring", "strategic planning",
}

# ─── Section Header Patterns ──────────────────────────────────────
SECTION_PATTERNS = {
    "experience": r"(?i)(?:work\s+)?experience|employment\s+history|professional\s+experience|work\s+history",
    "education": r"(?i)education|academic|qualifications|degrees",
    "skills": r"(?i)skills|technical\s+skills|competencies|technologies|expertise",
    "projects": r"(?i)projects|personal\s+projects|portfolio|key\s+projects",
    "certifications": r"(?i)certifications?|licenses?|accreditations?",
    "languages": r"(?i)languages",
    "summary": r"(?i)summary|objective|profile|about\s+me|professional\s+summary",
}

# ─── Regex Patterns ───────────────────────────────────────────────
EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
PHONE_PATTERN = re.compile(r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}")
LINKEDIN_PATTERN = re.compile(r"linkedin\.com/in/[\w-]+", re.IGNORECASE)
GITHUB_PATTERN = re.compile(r"github\.com/[\w-]+", re.IGNORECASE)
DATE_PATTERN = re.compile(
    r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|"
    r"Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
    r"\s*\d{4}|(?:\d{1,2}/\d{4})|(?:\d{4})\s*[-–—]\s*(?:Present|Current|\d{4})",
    re.IGNORECASE
)


def extract_text_from_pdf(content: bytes) -> str:
    """Extract text from PDF using PyMuPDF, with pdfplumber fallback."""
    text = ""

    # Primary: PyMuPDF (fitz)
    try:
        import fitz
        doc = fitz.open(stream=content, filetype="pdf")
        for page in doc:
            text += page.get_text() + "\n"
        doc.close()
        if text.strip():
            return text.strip()
    except Exception as e:
        logger.warning(f"PyMuPDF extraction failed: {e}")

    # Fallback: pdfplumber
    try:
        import pdfplumber
        import io
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        logger.warning(f"pdfplumber extraction failed: {e}")

    return text.strip()


def extract_text_from_docx(content: bytes) -> str:
    """Extract text from DOCX using python-docx."""
    try:
        import io
        from docx import Document
        doc = Document(io.BytesIO(content))
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text.strip()
    except Exception as e:
        logger.error(f"DOCX extraction failed: {e}")
        return ""


def extract_text(content: bytes, file_type: str) -> str:
    """Extract text from a resume file based on its type."""
    if file_type in ("pdf",):
        return extract_text_from_pdf(content)
    elif file_type in ("doc", "docx"):
        return extract_text_from_docx(content)
    return ""


def extract_email(text: str) -> Optional[str]:
    """Extract email address from text."""
    match = EMAIL_PATTERN.search(text)
    return match.group(0) if match else None


def extract_phone(text: str) -> Optional[str]:
    """Extract phone number from text."""
    match = PHONE_PATTERN.search(text)
    return match.group(0) if match else None


def extract_name(text: str) -> Optional[str]:
    """Extract name using spaCy NER or first line heuristic."""
    if SPACY_AVAILABLE and nlp:
        # Use first 500 chars for NER
        doc = nlp(text[:500])
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                name = ent.text.strip()
                # Validate it looks like a name (2+ words, no digits)
                if len(name.split()) >= 2 and not any(c.isdigit() for c in name):
                    return name

    # Fallback: first non-empty line that looks like a name
    for line in text.split("\n")[:5]:
        line = line.strip()
        if line and len(line.split()) >= 2 and len(line) < 50:
            if not EMAIL_PATTERN.search(line) and not PHONE_PATTERN.search(line):
                if not any(keyword in line.lower() for keyword in ["resume", "cv", "curriculum"]):
                    return line
    return None


def extract_address(text: str) -> Optional[str]:
    """Extract address using spaCy NER."""
    if SPACY_AVAILABLE and nlp:
        doc = nlp(text[:1000])
        locations = [ent.text for ent in doc.ents if ent.label_ in ("GPE", "LOC")]
        if locations:
            return ", ".join(locations[:3])
    return None


def extract_skills(text: str) -> list[str]:
    """Extract skills by matching against known skill databases."""
    text_lower = text.lower()
    found_skills = []

    for skill in TECHNICAL_SKILLS:
        # Use word boundary matching for single-word skills
        if len(skill.split()) == 1:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill)
        else:
            if skill in text_lower:
                found_skills.append(skill)

    for skill in SOFT_SKILLS:
        if skill in text_lower:
            found_skills.append(skill)

    return sorted(set(found_skills))


def _find_section(text: str, section_name: str) -> Optional[str]:
    """Find and extract a specific section from resume text."""
    pattern = SECTION_PATTERNS.get(section_name)
    if not pattern:
        return None

    lines = text.split("\n")
    start_idx = None
    end_idx = None

    for i, line in enumerate(lines):
        if re.search(pattern, line.strip()):
            start_idx = i + 1
            break

    if start_idx is None:
        return None

    # Find next section header
    for i in range(start_idx, len(lines)):
        for sec_name, sec_pattern in SECTION_PATTERNS.items():
            if sec_name != section_name and re.search(sec_pattern, lines[i].strip()):
                end_idx = i
                break
        if end_idx:
            break

    if end_idx is None:
        end_idx = len(lines)

    section_text = "\n".join(lines[start_idx:end_idx]).strip()
    return section_text if section_text else None


def extract_experience(text: str) -> list[dict]:
    """Extract work experience entries."""
    section = _find_section(text, "experience")
    if not section:
        return []

    entries = []
    current_entry = {}
    lines = section.split("\n")

    for line in lines:
        line = line.strip()
        if not line:
            if current_entry:
                entries.append(current_entry)
                current_entry = {}
            continue

        # Check if line contains a date range (likely a new entry)
        date_match = DATE_PATTERN.search(line)
        if date_match and (not current_entry or "title" in current_entry):
            if current_entry and "title" in current_entry:
                entries.append(current_entry)
            current_entry = {"title": line, "dates": date_match.group(0)}
        elif current_entry and "title" in current_entry:
            if "description" not in current_entry:
                current_entry["description"] = []
            current_entry["description"].append(line)

    if current_entry:
        entries.append(current_entry)

    return entries[:10]  # Limit to 10 entries


def extract_education(text: str) -> list[dict]:
    """Extract education entries."""
    section = _find_section(text, "education")
    if not section:
        return []

    entries = []
    current_entry = {}
    lines = section.split("\n")

    degree_keywords = ["bachelor", "master", "phd", "doctorate", "associate", "diploma",
                        "b.s.", "b.a.", "m.s.", "m.a.", "mba", "b.tech", "m.tech",
                        "b.e.", "m.e.", "b.sc", "m.sc"]

    for line in lines:
        line = line.strip()
        if not line:
            if current_entry:
                entries.append(current_entry)
                current_entry = {}
            continue

        line_lower = line.lower()
        if any(kw in line_lower for kw in degree_keywords):
            if current_entry:
                entries.append(current_entry)
            current_entry = {"degree": line}
            date_match = DATE_PATTERN.search(line)
            if date_match:
                current_entry["dates"] = date_match.group(0)
        elif current_entry:
            if "institution" not in current_entry:
                current_entry["institution"] = line
            else:
                current_entry.setdefault("details", []).append(line)

    if current_entry:
        entries.append(current_entry)

    return entries[:5]


def extract_projects(text: str) -> list[dict]:
    """Extract project entries."""
    section = _find_section(text, "projects")
    if not section:
        return []

    entries = []
    current_entry = {}
    lines = section.split("\n")

    for line in lines:
        line = line.strip()
        if not line:
            if current_entry:
                entries.append(current_entry)
                current_entry = {}
            continue

        if not current_entry:
            current_entry = {"name": line}
        else:
            current_entry.setdefault("description", []).append(line)

    if current_entry:
        entries.append(current_entry)

    return entries[:10]


def extract_certifications(text: str) -> list[str]:
    """Extract certifications."""
    section = _find_section(text, "certifications")
    if not section:
        return []
    return [line.strip() for line in section.split("\n") if line.strip()][:10]


def extract_languages(text: str) -> list[str]:
    """Extract languages."""
    section = _find_section(text, "languages")
    if not section:
        return []

    languages = []
    for line in section.split("\n"):
        line = line.strip()
        if line:
            # Split by common separators
            for lang in re.split(r"[,;|•·]", line):
                lang = lang.strip()
                if lang and len(lang) < 50:
                    languages.append(lang)
    return languages[:10]


def extract_summary(text: str) -> Optional[str]:
    """Extract professional summary/objective."""
    section = _find_section(text, "summary")
    if section:
        return section[:500]  # Limit to 500 chars
    return None


def parse_resume(content: bytes, file_type: str) -> dict:
    """
    Parse a resume file and extract all structured data.
    Returns a dictionary with all extracted fields.
    """
    raw_text = extract_text(content, file_type)
    if not raw_text:
        return {"raw_text": "", "error": "Could not extract text from file"}

    parsed_data = {
        "name": extract_name(raw_text),
        "email": extract_email(raw_text),
        "phone": extract_phone(raw_text),
        "address": extract_address(raw_text),
        "summary": extract_summary(raw_text),
        "skills": extract_skills(raw_text),
        "experience": extract_experience(raw_text),
        "education": extract_education(raw_text),
        "projects": extract_projects(raw_text),
        "certifications": extract_certifications(raw_text),
        "languages": extract_languages(raw_text),
    }

    return {
        "raw_text": raw_text,
        "parsed_data": parsed_data,
    }
