import re
import PyPDF2
import nltk
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

nltk.download("punkt")
nltk.download("stopwords")

nlp = spacy.load("en_core_web_sm")

# ---------------- PDF TEXT ---------------- #
def extract_text_from_pdf(uploaded_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

# ---------------- CLEAN TEXT ---------------- #
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

# ---------------- REMOVE STOPWORDS ---------------- #
def remove_stopwords(text):
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text)
    return " ".join([w for w in words if w not in stop_words])

# ---------------- LOAD SKILLS ---------------- #
def load_skills(file_path):
    with open(file_path, "r") as f:
        skills = f.read().splitlines()
    return skills

# ---------------- SKILL EXTRACTION ---------------- #
def extract_skills(text, skill_list):
    text = text.lower()
    found = []
    for skill in skill_list:
        if skill in text:
            found.append(skill)
    return list(set(found))

# ---------------- SECTION DETECTION ---------------- #
def detect_sections(text):
    sections = ["education", "experience", "skills", "projects"]
    found = []
    for sec in sections:
        if sec in text.lower():
            found.append(sec)
    return found

# ---------------- ATS SCORE ---------------- #
def ats_score(resume_skills, job_skills):
    if len(job_skills) == 0:
        return 0, []
    matched = set(resume_skills) & set(job_skills)
    score = len(matched) / len(job_skills) * 100
    return round(score, 2), list(matched)

# ---------------- SUGGESTIONS ---------------- #
def generate_suggestions(score, missing_skills, sections):
    suggestions = []

    if score < 50:
        suggestions.append("Increase skill match with job description")

    if missing_skills:
        suggestions.append(f"Add missing skills: {', '.join(missing_skills[:5])}")

    if "projects" not in sections:
        suggestions.append("Add a Projects section")

    if "experience" not in sections:
        suggestions.append("Add Experience section")

    return suggestions