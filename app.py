import streamlit as st
import PyPDF2
import re
import subprocess


from sentence_transformers import SentenceTransformer, util

# ================= LOAD MODEL =================
@st.cache_resource(show_spinner="Loading AI model...")
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()




# ================= PAGE CONFIG =================
st.set_page_config(page_title="AI-Powered Resume Analyzer and Career Chatbot System", layout="wide")

st.markdown("""
<h1 style='text-align: center; color: red;'>🚀 AI-Powered Resume Analyzer and Career Chatbot System</h1>
<p style='text-align: center; color: black;'>Smart Resume Matching & AI Career Guidance</p>
""", unsafe_allow_html=True)

# ================= SESSION STATE =================
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
    st.session_state.resume_text = ""
    st.session_state.job_desc = ""
    st.session_state.resume_skills = []
    st.session_state.jd_skills = []
    st.session_state.missing = []

# ================= INPUT =================
uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"],key="resume_upload")
job_desc = st.text_area("📝 Paste Job Description")

# # ================= SKILLS DATABASE =================
skill_bank = [
    # Programming
    "python", "java", "sql", "javascript",

    # Data Science
    "data analysis", "pandas", "numpy", "statistics",

    # Machine Learning
    "machine learning", "deep learning",
    "supervised learning", "unsupervised learning",
    "model training", "evaluation metrics",

    # NLP
    "natural language processing", "nlp",
    "transformers", "embeddings", "llm",
    "large language model", "prompt engineering",

    # Advanced AI
    "rag", "retrieval augmented generation",
    "vector database", "agentic ai", "ai agents",

    # Computer Vision
    "computer vision", "image classification",
    "object detection",

    # MLOps / Deployment
    "mlops", "docker", "kubernetes",
    "model deployment", "fastapi",

    # Frameworks
    "tensorflow", "pytorch", "scikit-learn",

    # Tools
    "git", "github"
]


@st.cache_resource
def build_skill_embeddings():
    return {
        skill: model.encode(skill, convert_to_tensor=True)
        for skill in skill_bank
    }

skill_embeddings = build_skill_embeddings()


skill_groups = {
    "llm": ["large language model", "llm"],
    "nlp": ["natural language processing", "nlp"],
    "cv": ["computer vision", "image classification", "object detection", "image processing"],
    "agents": ["ai agents", "agentic ai", "workflow orchestration"],
    "ml": ["machine learning", "supervised learning", "unsupervised learning"],
    "scikit learn": ["scikit-learn", "scikit learn", "sklearn"],
    "metrics": ["evaluation metrics", "metrics", "bias variance tradeoff"]
}


def normalize_skill(skill):
    skill = skill.lower().replace("-", " ")

    for key, values in skill_groups.items():
        for v in values:
            if v in skill:
                return key

    return skill




def is_similar(skill1, skill2):
    emb1 = model.encode(skill1, convert_to_tensor=True)
    emb2 = model.encode(skill2, convert_to_tensor=True)

    return util.cos_sim(emb1, emb2).item() > 0.75




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
    


def extract_skills_ai(text, skill_bank):

    found_skills = []

    sentences = text.split(".")

    # PRE-COMPUTE sentence embeddings once
    sentence_embeddings = [
        model.encode(sentence, convert_to_tensor=True)
        for sentence in sentences
        if sentence.strip()
    ]

    for skill in skill_bank:

        skill_embedding = skill_embeddings[skill]   # 🔥 reused (FAST)

        for sent_emb in sentence_embeddings:

            similarity = util.cos_sim(sent_emb, skill_embedding).item()

            if similarity > 0.55:
                found_skills.append(skill)
                break

    return sorted(set(found_skills))


def extract_skills(text, skill_bank):
    text = text.lower()
    found = []

    for skill in skill_bank:
        skill_clean = skill.replace("-", " ")
        pattern = r"\b" + re.escape(skill_clean) + r"\b"

        if re.search(pattern, text):
            found.append(normalize_skill(skill))

    return sorted(set(found))


# ================= CLEAN TEXT =================
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9+.#\s ]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# ================= EXTRACT PDF TEXT =================
def extract_text(file):
    text = ""

    try:
        reader = PyPDF2.PdfReader(file)

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "

    except Exception:
        return ""

    return clean_text(text)




# ================= ATS SCORE CALCULATION =================


def expand_skills(skills):
    expanded = set(skills)

    for key, values in skill_groups.items():
        if any(v in [s.lower() for s in skills] for v in values):
            expanded.add(key)

    return expanded


def soft_skill_match(resume_skills, jd_skills):
    if len(jd_skills) == 0:
        return 0

    score = 0
    total = len(jd_skills)

    # pre-encode resume skills once
    resume_embs = {
        r: model.encode(r, convert_to_tensor=True)
        for r in resume_skills
    }

    for skill in jd_skills:
        skill_emb = model.encode(skill, convert_to_tensor=True)

        for r in resume_skills:
            sim = util.cos_sim(skill_emb, resume_embs[r]).item()

            if sim > 0.75:
                score += 1
                break

    return score / total



def calculate_ats_ai(resume_text, resume_skills, jd_skills):

    if not jd_skills:
        return 0

    resume_set = expand_skills(resume_skills)
    jd_set = expand_skills(jd_skills)

    # COVERAGE
    coverage = soft_skill_match(resume_skills, jd_skills)
    score1 = coverage * 60

    # SEMANTIC
    resume_vec = model.encode(list(resume_set), convert_to_tensor=True).mean(dim=0)
    jd_vec = model.encode(list(jd_set), convert_to_tensor=True).mean(dim=0)

    semantic = util.cos_sim(resume_vec, jd_vec).item()
    semantic = max(0, min(semantic, 1.0))
    score2 = semantic * 25

    # READABILITY
    score3 = min(len(resume_text.split()) / 300, 1) * 15

    return int(score1 + score2 + score3)


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

        # STEP 1: extract skills
        resume_skills = extract_skills(resume_text, skill_bank)
        jd_skills = extract_skills(job_desc, skill_bank)

        # STEP 2: normalize FIRST
        resume_skills = [normalize_skill(s) for s in resume_skills]
        jd_skills = [normalize_skill(s) for s in jd_skills]

        # STEP 3: remove duplicates
        resume_skills = list(set([normalize_skill(s) for s in resume_skills]))
        jd_skills = list(set([normalize_skill(s) for s in jd_skills]))

        # STEP 4: ATS SCORE
        ats_score = calculate_ats_ai(resume_text,resume_skills, jd_skills)

        # STEP 5: AI MATCH SCORE
        ai_score = int(
            util.cos_sim(
                model.encode(resume_text, convert_to_tensor=True),
                model.encode(job_desc, convert_to_tensor=True)
            ).item() * 100
        )

        # STEP 6: missing skills
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

       

        


            