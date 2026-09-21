import re
from PyPDF2 import PdfReader


# Technical skills that ResumeMatch can recognize
SKILLS = {
    "python": ["python"],
    "java": ["java"],
    "c++": ["c++"],
    "c#": ["c#"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript"],
    "html": ["html", "html5"],
    "css": ["css", "css3"],
    "sql": ["sql"],
    "react": ["react", "react.js", "reactjs"],
    "angular": ["angular"],
    "vue": ["vue", "vue.js", "vuejs"],
    "node.js": ["node.js", "nodejs"],
    "flask": ["flask"],
    "django": ["django"],
    "fastapi": ["fastapi"],
    "spring boot": ["spring boot"],
    "git": ["git"],
    "github": ["github"],
    "gitlab": ["gitlab"],
    "aws": ["aws", "amazon web services"],
    "azure": ["azure", "microsoft azure"],
    "docker": ["docker"],
    "kubernetes": ["kubernetes"],
    "linux": ["linux"],
    "mongodb": ["mongodb"],
    "mysql": ["mysql"],
    "postgresql": ["postgresql", "postgres"],
    "sqlite": ["sqlite"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "machine learning": ["machine learning"],
    "data analysis": ["data analysis"],
    "data visualization": ["data visualization"],
    "power bi": ["power bi"],
    "tableau": ["tableau"],
    "excel": ["excel", "microsoft excel"],
    "rest api": ["rest api", "restful api", "restful apis"],
    "json": ["json"],
    "ci/cd": ["ci/cd", "continuous integration", "continuous delivery"],
    "agile": ["agile"],
    "data structures": ["data structures"],
    "algorithms": ["algorithms"]
}


def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + " "

    return text


def contains_skill(text, skill_variations):
    text = text.lower()

    for variation in skill_variations:
        variation = variation.lower()

        pattern = r"(?<!\w)" + re.escape(variation) + r"(?!\w)"

        if re.search(pattern, text):
            return True

    return False


def analyze_resume(resume_text, job_description):
    matched_skills = []
    missing_skills = []
    required_skills = []

    for skill, variations in SKILLS.items():

        if contains_skill(job_description, variations):
            required_skills.append(skill)

            if contains_skill(resume_text, variations):
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