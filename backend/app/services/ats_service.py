"""
ATS Scoring Engine — evaluates resumes against ATS criteria.
"""
import re
from typing import Optional

from app.core.logging import get_logger

logger = get_logger(__name__)

# Industry keyword lists for different sectors
INDUSTRY_KEYWORDS = {
    "software_engineering": [
        "agile", "scrum", "ci/cd", "devops", "microservices", "api", "rest",
        "cloud", "aws", "azure", "gcp", "docker", "kubernetes", "testing",
        "unit test", "integration", "deployment", "monitoring", "scalable",
        "performance", "optimization", "architecture", "design patterns",
        "version control", "git", "code review", "debugging",
    ],
    "data_science": [
        "machine learning", "deep learning", "statistics", "data analysis",
        "visualization", "python", "r", "sql", "tensorflow", "pytorch",
        "model", "algorithm", "feature engineering", "a/b testing",
        "regression", "classification", "clustering", "nlp", "big data",
    ],
    "general": [
        "managed", "led", "developed", "implemented", "designed", "created",
        "improved", "increased", "reduced", "achieved", "delivered",
        "collaborated", "coordinated", "analyzed", "optimized", "maintained",
        "supervised", "trained", "established", "generated", "resolved",
    ],
}

# Action verbs that ATS systems look for
ACTION_VERBS = {
    "achieved", "administered", "analyzed", "built", "collaborated",
    "coordinated", "created", "delivered", "designed", "developed",
    "directed", "enhanced", "established", "executed", "facilitated",
    "generated", "implemented", "improved", "increased", "launched",
    "led", "managed", "mentored", "negotiated", "optimized",
    "organized", "oversaw", "planned", "produced", "reduced",
    "resolved", "spearheaded", "streamlined", "supervised", "trained",
}


def score_contact_info(parsed_data: dict) -> tuple[float, list[str]]:
    """Score contact information completeness (5% weight)."""
    score = 0
    suggestions = []

    if parsed_data.get("email"):
        score += 40
    else:
        suggestions.append("Add a professional email address")

    if parsed_data.get("phone"):
        score += 30
    else:
        suggestions.append("Add a phone number")

    if parsed_data.get("name"):
        score += 20
    else:
        suggestions.append("Ensure your full name is clearly visible at the top")

    if parsed_data.get("address"):
        score += 10
    else:
        suggestions.append("Consider adding your city and state/country")

    return min(score, 100), suggestions


def score_formatting(raw_text: str, parsed_data: dict) -> tuple[float, list[str]]:
    """Score document formatting (15% weight)."""
    score = 0
    suggestions = []
    lines = raw_text.split("\n")
    non_empty_lines = [l for l in lines if l.strip()]

    # Check length (ideal: 300-800 words for 1-2 pages)
    word_count = len(raw_text.split())
    if 300 <= word_count <= 1000:
        score += 25
    elif word_count < 200:
        suggestions.append("Resume is too short — aim for at least 300 words")
        score += 10
    elif word_count > 1200:
        suggestions.append("Resume may be too long — consider condensing to 1-2 pages")
        score += 15
    else:
        score += 20

    # Check section headers present
    sections_found = 0
    important_sections = ["experience", "education", "skills"]
    for section in important_sections:
        for line in non_empty_lines:
            if re.search(r"(?i)\b" + section + r"\b", line):
                sections_found += 1
                break

    if sections_found >= 3:
        score += 25
    elif sections_found >= 2:
        score += 15
        suggestions.append("Add clear section headers for Experience, Education, and Skills")
    else:
        score += 5
        suggestions.append("Include clear section headers (Experience, Education, Skills)")

    # Check for bullet points
    bullet_lines = sum(1 for l in lines if l.strip().startswith(("•", "-", "·", "▪", "►", "*")))
    if bullet_lines >= 5:
        score += 25
    elif bullet_lines >= 2:
        score += 15
        suggestions.append("Use more bullet points to describe your experience")
    else:
        score += 5
        suggestions.append("Use bullet points instead of paragraphs for better readability")

    # Check for consistent formatting (no excessive blank lines)
    consecutive_blanks = max(
        (len(list(g)) for k, g in __import__("itertools").groupby(lines, key=lambda x: x.strip() == "") if k),
        default=0
    )
    if consecutive_blanks <= 2:
        score += 25
    elif consecutive_blanks <= 4:
        score += 15
    else:
        score += 5
        suggestions.append("Reduce excessive white space between sections")

    return min(score, 100), suggestions


def score_skills(parsed_data: dict) -> tuple[float, list[str]]:
    """Score skills section (20% weight)."""
    score = 0
    suggestions = []
    skills = parsed_data.get("skills", [])

    if len(skills) >= 10:
        score += 50
    elif len(skills) >= 5:
        score += 30
        suggestions.append("Add more relevant skills (aim for 10-15)")
    elif len(skills) >= 1:
        score += 15
        suggestions.append("Include more technical and soft skills")
    else:
        suggestions.append("Add a dedicated Skills section with relevant competencies")

    # Check for mix of technical and soft skills
    from app.services.parser_service import TECHNICAL_SKILLS, SOFT_SKILLS
    tech_count = sum(1 for s in skills if s.lower() in TECHNICAL_SKILLS)
    soft_count = sum(1 for s in skills if s.lower() in SOFT_SKILLS)

    if tech_count >= 3 and soft_count >= 1:
        score += 30
    elif tech_count >= 3:
        score += 20
        suggestions.append("Include some soft skills (leadership, communication, teamwork)")
    elif tech_count >= 1:
        score += 10
        suggestions.append("Add more technical skills relevant to your target role")
    else:
        suggestions.append("Include both technical and soft skills")

    # Bonus for organized skills
    if len(skills) >= 5:
        score += 20
    else:
        score += 10

    return min(score, 100), suggestions


def score_experience(raw_text: str, parsed_data: dict) -> tuple[float, list[str]]:
    """Score work experience section (20% weight)."""
    score = 0
    suggestions = []
    experience = parsed_data.get("experience", [])

    if len(experience) >= 3:
        score += 30
    elif len(experience) >= 1:
        score += 15
        suggestions.append("Include more work experience entries if available")
    else:
        suggestions.append("Add a Work Experience section with your professional history")

    # Check for action verbs
    text_lower = raw_text.lower()
    action_verb_count = sum(1 for verb in ACTION_VERBS if verb in text_lower)

    if action_verb_count >= 8:
        score += 25
    elif action_verb_count >= 4:
        score += 15
        suggestions.append("Use more action verbs (led, developed, implemented, achieved)")
    else:
        score += 5
        suggestions.append("Start bullet points with strong action verbs")

    # Check for quantifiable achievements (numbers, percentages)
    number_pattern = re.compile(r'\d+[%$]|\$\d+|\d+\+')
    numbers_found = len(number_pattern.findall(raw_text))

    if numbers_found >= 5:
        score += 25
    elif numbers_found >= 2:
        score += 15
        suggestions.append("Add more quantifiable achievements (e.g., 'increased sales by 20%')")
    else:
        score += 5
        suggestions.append("Quantify your accomplishments with numbers and percentages")

    # Check for date ranges
    from app.services.parser_service import DATE_PATTERN
    dates_found = len(DATE_PATTERN.findall(raw_text))
    if dates_found >= 2:
        score += 20
    elif dates_found >= 1:
        score += 10
    else:
        suggestions.append("Include date ranges for each position")

    return min(score, 100), suggestions


def score_education(parsed_data: dict) -> tuple[float, list[str]]:
    """Score education section (10% weight)."""
    score = 0
    suggestions = []
    education = parsed_data.get("education", [])

    if len(education) >= 1:
        score += 50

        # Check for degree
        has_degree = any("degree" in str(e).lower() or
                         any(kw in str(e).lower() for kw in
                             ["bachelor", "master", "phd", "b.s.", "b.a.", "m.s.", "mba", "b.tech"])
                         for e in education)
        if has_degree:
            score += 25
        else:
            suggestions.append("Clearly state your degree (e.g., Bachelor of Science in Computer Science)")

        # Check for institution
        has_institution = any("institution" in e for e in education if isinstance(e, dict))
        if has_institution:
            score += 25
        else:
            score += 15
    else:
        suggestions.append("Add an Education section with your academic qualifications")

    return min(score, 100), suggestions


def score_keywords(raw_text: str) -> tuple[float, list[str], list[str]]:
    """Score industry keyword usage (15% weight). Returns score, suggestions, missing keywords."""
    score = 0
    suggestions = []
    missing_keywords = []
    text_lower = raw_text.lower()

    # Check against general action/impact keywords
    general_found = 0
    general_missing = []
    for kw in INDUSTRY_KEYWORDS["general"]:
        if kw in text_lower:
            general_found += 1
        else:
            general_missing.append(kw)

    keyword_ratio = general_found / len(INDUSTRY_KEYWORDS["general"]) if INDUSTRY_KEYWORDS["general"] else 0

    if keyword_ratio >= 0.5:
        score += 50
    elif keyword_ratio >= 0.3:
        score += 30
        suggestions.append("Use more industry-standard action verbs and keywords")
    else:
        score += 10
        suggestions.append("Include more relevant keywords used in job descriptions")

    # Check technical keywords
    tech_found = 0
    for kw_list in [INDUSTRY_KEYWORDS["software_engineering"], INDUSTRY_KEYWORDS["data_science"]]:
        for kw in kw_list:
            if kw in text_lower:
                tech_found += 1

    if tech_found >= 10:
        score += 50
    elif tech_found >= 5:
        score += 30
    elif tech_found >= 1:
        score += 15
    else:
        suggestions.append("Add technical/industry-specific keywords relevant to your target role")

    # Collect top missing keywords
    missing_keywords = general_missing[:10]

    return min(score, 100), suggestions, missing_keywords


def score_projects(parsed_data: dict) -> tuple[float, list[str]]:
    """Score projects section (10% weight)."""
    score = 0
    suggestions = []
    projects = parsed_data.get("projects", [])

    if len(projects) >= 3:
        score += 60
    elif len(projects) >= 1:
        score += 30
        suggestions.append("Add more projects to showcase your practical experience")
    else:
        suggestions.append("Include a Projects section with personal or professional projects")
        return 20, suggestions  # Minimum score

    # Check for descriptions
    described = sum(1 for p in projects if isinstance(p, dict) and p.get("description"))
    if described >= 2:
        score += 40
    elif described >= 1:
        score += 20
        suggestions.append("Add detailed descriptions to all projects")
    else:
        suggestions.append("Include technologies used and your role in each project")

    return min(score, 100), suggestions


def score_grammar(raw_text: str) -> tuple[float, list[str]]:
    """Basic grammar and readability scoring (5% weight)."""
    score = 70  # Default reasonable score
    suggestions = []

    # Check sentence length
    sentences = re.split(r'[.!?]+', raw_text)
    long_sentences = sum(1 for s in sentences if len(s.split()) > 30)

    if long_sentences == 0:
        score += 15
    elif long_sentences <= 3:
        score += 5
    else:
        suggestions.append("Break up long sentences for better readability")

    # Check for first-person pronouns (should be minimal in resumes)
    pronoun_count = len(re.findall(r'\b(?:I|me|my|mine)\b', raw_text, re.IGNORECASE))
    if pronoun_count <= 2:
        score += 15
    elif pronoun_count <= 5:
        score += 5
    else:
        suggestions.append("Minimize use of first-person pronouns (I, me, my)")

    return min(score, 100), suggestions


def calculate_ats_score(raw_text: str, parsed_data: dict) -> dict:
    """
    Calculate comprehensive ATS score with weighted categories.
    Returns overall score, section scores, suggestions, and missing keywords.
    """
    # Calculate each section
    contact_score, contact_suggestions = score_contact_info(parsed_data)
    formatting_score, formatting_suggestions = score_formatting(raw_text, parsed_data)
    skills_score, skills_suggestions = score_skills(parsed_data)
    experience_score, experience_suggestions = score_experience(raw_text, parsed_data)
    education_score, education_suggestions = score_education(parsed_data)
    keywords_score, keywords_suggestions, missing_keywords = score_keywords(raw_text)
    projects_score, projects_suggestions = score_projects(parsed_data)
    grammar_score, grammar_suggestions = score_grammar(raw_text)

    # Weighted overall score
    weights = {
        "contact_info": 0.05,
        "formatting": 0.15,
        "skills": 0.20,
        "experience": 0.20,
        "education": 0.10,
        "keywords": 0.15,
        "projects": 0.10,
        "grammar": 0.05,
    }

    section_scores = {
        "contact_info": round(contact_score, 1),
        "formatting": round(formatting_score, 1),
        "skills": round(skills_score, 1),
        "experience": round(experience_score, 1),
        "education": round(education_score, 1),
        "keywords": round(keywords_score, 1),
        "projects": round(projects_score, 1),
        "grammar": round(grammar_score, 1),
    }

    overall_score = sum(
        section_scores[key] * weights[key] for key in weights
    )

    # Collect all suggestions
    all_suggestions = (
        contact_suggestions + formatting_suggestions + skills_suggestions +
        experience_suggestions + education_suggestions + keywords_suggestions +
        projects_suggestions + grammar_suggestions
    )

    return {
        "overall_score": round(overall_score, 1),
        "section_scores": section_scores,
        "missing_keywords": missing_keywords,
        "suggestions": all_suggestions,
    }
