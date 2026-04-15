import streamlit as st
import PyPDF2
import re
import subprocess

# ================= PAGE CONFIG =================
st.set_page_config(page_title="AI-Powered Resume Analyzer and Career Chatbot System", layout="wide")

st.markdown("""
<h1 style='text-align: center; color: red;'>🚀 AI-Powered Resume Analyzer and Career Chatbot System</h1>
<p style='text-align: center; color: black;'>Smart Resume Matching & AI Career Guidance</p>
""", unsafe_allow_html=True)

# ================= SESSION STATE =================
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

# ================= INPUT =================
uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])
job_desc = st.text_area("📝 Paste Job Description")

# ================= SKILLS DATABASE =================
skills_db = [
    "python", "machine learning", "deep learning", "nlp",
    "tensorflow", "pytorch", "sql", "pandas", "numpy",
    "flask", "fastapi", "data analysis", "git",
    "scikit-learn", "matplotlib", "seaborn"
]


st.markdown("""
<style>

/* ================= MAIN BACKGROUND ================= */
body {
    background-color: #ffffff;
    color: #000000;
}

.stApp {
    background-color: #ffffff;
}

/* ================= SIDEBAR ================= */
section[data-testid="stSidebar"] {
    background-color: #0A66C2;  /* Blue */
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* ================= BUTTONS ================= */
.stButton>button {
    background-color: #0A66C2;
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 100%;
    transition: 0.3s;
}

.stButton>button:hover {
    background-color: #084a91;
    color: white;
}

/* ================= INPUT FIELDS ================= */
.stTextInput input, .stTextArea textarea {
    border-radius: 8px;
    border: 1px solid #0A66C2;
    background-color: #0A66C2;  /* Blue */;
    color: black;
}

/* Add padding inside textarea */
textarea {
    padding: 10px;
    color: white !important;
}

/* ================= FILE UPLOADER ================= */
[data-testid="stFileUploader"] {
    border: 1px solid #0A66C2;
    border-radius: 10px;
    padding: 10px;
    background-color: #0A66C2;  /* Blue */;
    color: white !important;
}

/* File uploader label */
label[data-testid="stFileUploaderLabel"] {
    color: black !important;
    font-weight: 600;
}

/* Text area label */
label[data-testid="stTextAreaLabel"] {
    color: black !important;
    font-weight: 600;
}

/* Improve label spacing */
label {
    margin-bottom: 5px;
    display: block;
    color: black !important;
}

/* ================= METRIC CARDS ================= */
[data-testid="stMetric"] {
    background-color: black;
    border-radius: 10px;
    padding: 10px;
    border: 1px solid #0A66C2;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
            


/* Metric label (AI Match %, ATS Score %) */
[data-testid="stMetricLabel"] {
    color: black !important;
}

/* Metric value (number) */
[data-testid="stMetricValue"] {
    color: black !important;
    font-size: 28px;
    font-weight: bold;
}

/* Metric container */
[data-testid="stMetric"] {
    background-color: #ffffff !important;
    border: 1px solid #0A66C2;
    border-radius: 15px;
    padding: 15px;
}
            


/* ================= HEADINGS ================= */
h1, h2, h3 {
    color: #0A66C2;
}

/* ================= DIVIDER ================= */
hr {
    border: 1px solid #e6f0ff;
}

/* ================= SCROLLBAR (OPTIONAL) ================= */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #0A66C2;
    border-radius: 10px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
}

</style>
""", unsafe_allow_html=True)




with st.sidebar:

    st.title("📊 Dashboard")

    st.markdown("""
    ### 👋 Welcome

    This AI Resume Analyzer helps you:

    ✔ Analyze your resume  
    ✔ Match with job description  
    ✔ Identify missing skills  
    ✔ Get AI career advice  

    ---

    ### 🚀 How to Use

    1. Upload your resume  
    2. Paste job description  
    3. Click **Analyze Resume**  
    4. Ask AI for improvements  

    ---

    ### 💡 Tips

    - Use updated resume  
    - Add projects & skills  
    - Tailor for each job  

    """)

    st.markdown("---")
    st.caption("Built by Indra 🚀")


# ================= CLEAN TEXT =================
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9+.# ]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# ================= EXTRACT PDF TEXT =================
def extract_text(file):
    text = ""
    reader = PyPDF2.PdfReader(file)

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    return clean_text(text)

# ================= RESUME SKILLS =================
def extract_resume_skills(text):
    found = []

    for skill in skills_db:
        if re.search(rf"\b{re.escape(skill)}\b", text):
            found.append(skill)

    return sorted(list(set(found)))

# ================= JOB SKILLS (FIXED) =================
def extract_job_skills(text):
    found = []
    text = text.lower()

    for skill in skills_db:
        if skill in text:
            found.append(skill)

    return sorted(list(set(found)))

# ================= FORMAT AI OUTPUT (ADD HERE) =================
def format_ai_output(text):
    lines = text.split("\n")

    bullets = []

    for line in lines:
        line = line.strip()

        # keep only bullet lines
        if line.startswith("-") or line.startswith("•"):
            line = line.lstrip("-• ").strip()
            if line:
                bullets.append(line)

    return "\n".join(bullets)

# ================= AI COACH =================
def ask_ai(question, resume_text, job_desc):

    prompt = f"""
SYSTEM:
You are a strict resume evaluation engine for AI/ML hiring.

You MUST follow formatting rules exactly. No exceptions.

Your job:
- Evaluate resume brutally and realistically
- Focus only on job-relevant gaps
- Give actionable improvement points

RULES (STRICT - MUST FOLLOW):

- Output ONLY bullet points (4 to 5 max)
- Each bullet MUST start with "- "
- Do NOT include numbering (1,2,3,etc.)
- Do NOT include any headings, titles, or explanations
- Do NOT write any text before or after bullets

- Each bullet MUST be a single complete sentence
- Do NOT break sentences into multiple lines under any condition
- Do NOT split words (e.g., TensorFlow/PyTorch must remain intact)
- Do NOT repeat words, phrases, or ideas

- Keep language simple, professional, and recruiter-friendly
- Focus ONLY on resume vs job description gaps
- No paragraphs allowed
- No extra formatting, symbols, or emojis

- No paragraphs allowed
- Do NOT write continuous paragraph text
- If you cannot follow this, output nothing

RESUME:
{resume_text[:2000]}

JOB DESCRIPTION:
{job_desc[:2000]}

QUESTION:
{question}
"""

    try:
        result = subprocess.run(
            ["ollama", "run", "mistral"],
            input=prompt,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="ignore",
            timeout=180
        )

        output = result.stdout.strip()

        # 🔥 STEP 1: remove ANSI garbage
        output = re.sub(r"\x1b\[[0-9;]*[a-zA-Z]", "", output)

        # 🔥 STEP 2: remove weird unicode / duplication issues
        output = re.sub(r"(\b\w+\b)(\s+\1)+", r"\1", output)

        # 🔥 STEP 3: remove non-ascii noise
        output = re.sub(r"[^\x00-\x7F]+", " ", output)

        # 🔥 STEP 4: clean spaces
        output = re.sub(r"[ \t]+", " ", output)

        return output

    except subprocess.TimeoutExpired:
        return "AI is taking too long. Try again."

    except Exception as e:
        return f"Error: {str(e)}"

# ================= ANALYZE BUTTON =================
if st.button("🔍 Analyze Resume"):

    if uploaded_file and job_desc.strip():

        resume_text = extract_text(uploaded_file)

        # FIXED LOGIC
        resume_skills = extract_resume_skills(resume_text)
        jd_skills = extract_job_skills(job_desc)

        match = len(set(resume_skills) & set(jd_skills))
        total = len(jd_skills)

        ai_score = int((match / total) * 100) if total > 0 else 0
        ats_score = int((len(resume_skills) / len(skills_db)) * 100)

        missing = list(set(jd_skills) - set(resume_skills))

        # STORE STATE
        st.session_state.analysis_done = True
        st.session_state.resume_text = resume_text
        st.session_state.job_desc = job_desc
        st.session_state.resume_skills = resume_skills
        st.session_state.jd_skills = jd_skills
        st.session_state.missing = missing
        st.session_state.ai_score = ai_score
        st.session_state.ats_score = ats_score

    else:
        st.warning("⚠️ Please upload resume and paste job description")


st.markdown("---")


# ================= RESULTS =================
if st.session_state.analysis_done:

    st.markdown("<h2 style='color:black;'>📊 Results</h2>", unsafe_allow_html=True)


    col1, col2 = st.columns(2)

    with col1:
       st.metric("AI Match %", st.session_state.ai_score)
       st.markdown(
    "<p style='color:black; font-weight:500; font-size:13px;'>Measures how closely your resume matches the job requirements.</p>",
    unsafe_allow_html=True
)

    with col2:
       st.metric("ATS Score %", st.session_state.ats_score)
       st.markdown(
    "<p style='color:black; font-weight:500; font-size:13px;'>Shows how well your resume is optimized for ATS systems.</p>",
    unsafe_allow_html=True
       )

    

    st.markdown("<h3 style='color:black;'>✅ Skills Found (Resume)</h3>", unsafe_allow_html=True)
    st.write(st.session_state.resume_skills)

    st.markdown("<h3 style='color:black;'>📌 Skills Required (Job)</h3>", unsafe_allow_html=True)
    st.write(st.session_state.jd_skills)

    st.markdown("<h3 style='color:black;'>❌ Missing Skills</h3>", unsafe_allow_html=True)
    st.write(st.session_state.missing)

     # Match message
    if st.session_state.ai_score >= 70:
        st.markdown("<p style='color:green; font-weight:bold;'>Strong Match - Good chance for interview</p>", unsafe_allow_html=True)
    elif st.session_state.ai_score >= 40:
        st.markdown("<p style='color:orange; font-weight:bold;'>Average Match - Improve your skills</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='color:red; font-weight:bold;'>Low Match - Needs improvement</p>", unsafe_allow_html=True)

# ================= AI COACH =================
if st.session_state.analysis_done:
    
    st.markdown(
    "<h3 style='color:black;'>🤖 AI Career Chatbot</h3>",
    unsafe_allow_html=True
)    

    questions = [
        "What should I improve in my resume?",
        "Am I fit for this job?",
        "What skills should I learn next?",
        "What projects should I add?",
        "How can I improve ATS score?"
    ]

    question = st.selectbox("Select Question", questions)

    if st.button("💬 Ask AI"):

        with st.spinner("Thinking..."):
            answer = ask_ai(
                question,
                st.session_state.resume_text,
                st.session_state.job_desc
            )

        cleaned = format_ai_output(answer)

        for line in cleaned.split("\n"):
            if line.strip():
                 st.markdown(
   f"""
            <div style="
                background:#f5f9ff;
                color:black;
                padding:10px 12px;
                margin-bottom:8px;
                border-left:4px solid #0A66C2;
                border-radius:8px;
                font-size:14px;
                line-height:1.5;
            ">
        • {line.strip()}
    </div>
    """,
    unsafe_allow_html=True
)

       

        


            