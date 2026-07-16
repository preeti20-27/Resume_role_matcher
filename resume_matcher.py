"""
Resume Role Matcher
Extracts text, name, and email from a PDF resume, matches found skills
against known job roles, and returns a percentage match score per role.
"""

import re
import fitz  # PyMuPDF
import spacy

nlp = spacy.load("en_core_web_sm")


def extract_text_from_pdf(file_path: str) -> str:
    """Reads all text content from a PDF resume."""
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text


def clean_text(text: str) -> str:
    """Strips non-alphanumeric characters and normalizes whitespace."""
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize_and_filter(text: str) -> list[str]:
    """Lemmatizes and removes stopwords/punctuation using spaCy."""
    doc = nlp(text)
    return [token.lemma_.lower() for token in doc if not token.is_stop and token.is_alpha]


def extract_name(text: str) -> str:
    """Naive name extraction: assumes the resume's first line is the name."""
    lines = text.strip().split("\n")
    return lines[0] if lines else "Name not found"


def extract_email(text: str) -> str:
    """Extracts the first email-like pattern found in the resume."""
    match = re.search(r"[\w.-]+@[\w.-]+", text)
    return match.group(0) if match else "Email not found"


def extract_skills(text: str, known_skills: list[str]) -> list[str]:
    """Returns which known skills appear anywhere in the resume text."""
    text_lower = text.lower()
    found = [skill for skill in known_skills if skill.lower() in text_lower]
    return list(set(found))


def match_job_roles(skills_found: list[str], job_roles: dict[str, list[str]]) -> dict[str, str]:
    """Scores each job role by the percentage of its required skills that were found."""
    scores = {}
    for role, role_skills in job_roles.items():
        match_count = len(set(skills_found) & set(role_skills))
        total = len(role_skills)
        score = round((match_count / total) * 100, 2) if total else 0
        scores[role] = f"{score}% match"
    return scores


def analyze_resume(resume_path: str, skills: list[str], job_roles: dict[str, list[str]]) -> dict:
    """Runs the full pipeline: PDF -> cleaned text -> extracted fields -> role match scores."""
    text = extract_text_from_pdf(resume_path)
    cleaned = clean_text(text)
    tokens = tokenize_and_filter(cleaned)
    name = extract_name(text)
    email = extract_email(text)
    skills_found = extract_skills(text, skills)
    matched_roles = match_job_roles(skills_found, job_roles)

    result = {
        "name": name,
        "email": email,
        "skills_found": skills_found,
        "role_match_scores": matched_roles,
        "token_count": len(tokens),
    }

    print("Name:", result["name"])
    print("Email:", result["email"])
    print("Skills Found:", result["skills_found"])
    print("Role Match Scores:", result["role_match_scores"])

    return result


if __name__ == "__main__":
    KNOWN_SKILLS = [
        "Python", "SQL", "Data Analysis", "Machine Learning", "NLP",
        "Communication", "Java", "C++", "Excel", "Deep Learning",
    ]

    JOB_ROLES = {
        "Data Analyst": ["Python", "SQL", "Excel", "Data Analysis"],
        "Machine Learning Engineer": ["Python", "Machine Learning", "Deep Learning", "NLP"],
        "Software Developer": ["Java", "C++", "Communication"],
    }

    analyze_resume("Fake_Resume_John_Doe.pdf", KNOWN_SKILLS, JOB_ROLES)
