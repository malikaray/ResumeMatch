import re
from PyPDF2 import PdfReader


SKILLS = [
    "python", "java", "c++", "javascript",
    "html", "css", "sql", "react",
    "git", "github", "aws", "docker",
    "linux", "excel", "power bi", "tableau",
    "flask", "django", "fastapi",
    "node.js", "mongodb", "mysql",
    "postgresql", "azure", "tensorflow",
    "pytorch", "pandas", "numpy",
    "machine learning", "data analysis",
    "data visualization", "rest api",
    "kubernetes"
]


def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + " "

    return text


def contains_skill(text, skill):
    text = text.lower()
    skill = skill.lower()

    pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

    return re.search(pattern, text) is not None


def analyze_resume(resume_text, job_description):

    matched_skills = []
    missing_skills = []
    required_skills = []

    for skill in SKILLS:

        if contains_skill(job_description, skill):

            required_skills.append(skill)

            if contains_skill(resume_text, skill):
                matched_skills.append(skill)

            else:
                missing_skills.append(skill)

    total_required = len(required_skills)

    if total_required > 0:
        match_percentage = (
            len(matched_skills) / total_required
        ) * 100
    else:
        match_percentage = 0

    match_percentage = round(match_percentage, 1)

    if match_percentage >= 80:
        recommendation = (
            "Excellent match! Your resume contains most "
            "of the technical skills requested for this position."
        )

    elif match_percentage >= 60:
        recommendation = (
            "Good match. Consider highlighting experience "
            "with the missing skills before applying."
        )

    elif match_percentage >= 40:
        recommendation = (
            "Moderate match. Consider strengthening or "
            "highlighting some of the missing skills."
        )

    else:
        recommendation = (
            "Your resume currently has a lower technical-skill "
            "match for this position. Review the missing skills "
            "and look for relevant experience you can truthfully highlight."
        )

    return {
        "score": match_percentage,
        "matched": matched_skills,
        "missing": missing_skills,
        "required": required_skills,
        "recommendation": recommendation
    }