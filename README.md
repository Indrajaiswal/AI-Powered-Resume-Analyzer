## 🧠 AI Resume Analyzer & Career Chatbot | Python, Streamlit, NLP, LLMs
- Built an AI-powered resume analysis web application that evaluates resumes against job descriptions using NLP-based skill extraction and matching algorithms.
- Implemented an ATS scoring system to measure resume compatibility with job requirements based on extracted skills and keyword matching.
- Developed a Generative AI career coach using local LLM (Ollama/Mistral) to provide personalized, structured resume improvement suggestions.
- Designed an interactive Streamlit dashboard with real-time resume upload, job description parsing, and dynamic AI feedback visualization.
- Improved user experience with custom UI styling, bullet-based AI responses, and structured career guidance formatting.

## 📌 Overview

- The AI Resume Analyzer & Career Chatbot is a smart AI-powered web application that analyzes resumes, compares them with job descriptions, calculates match scores (AI Match & ATS Score), and provides personalized career improvement suggestions using an AI chatbot.

- It helps students and job seekers improve their resumes and increase their chances of getting shortlisted.


## ✨ Features
- 📄 Upload and analyze PDF resumes
- 🧠 Extract skills using NLP-based matching
- 📊 AI Match Score (Resume vs Job Description)
- 📈 ATS Score (Resume optimization level)
- ❌ Missing skills detection
- 🤖 AI Career Coach chatbot for personalized suggestions
- 💬 Interactive Q&A system for resume improvement
- 🎯 Real-time feedback on resume quality



## 🛠️ Tech Stack
- Python 🐍
- Streamlit 🎈
- NLP (Regex-based skill extraction)
- PyPDF2 (Resume parsing)
- Ollama / Mistral LLM (AI chatbot)
- HTML + CSS (UI styling)


## Project Structure
| File / Folder      | Description                                                  |
| ------------------ | ------------------------------------------------------------ |
| `app.py`           | Main Streamlit application file (UI + workflow)              |
| `utils.py`         | Helper functions for skill extraction, parsing, and AI logic |
| `model/`           | Contains AI scoring and matching logic                       |
| `requirements.txt` | List of Python dependencies required to run the project      |
| `.gitignore`       | Specifies files/folders to ignore (e.g., venv, cache files)  |
| `README.md`        | Project documentation with setup and usage instructions      |




## ⚙️ How It Works
- Upload your resume (PDF)
- Paste job description
- System extracts skills from both
- AI calculates:
- Match percentage
- ATS score
- Missing skills
- AI chatbot suggests improvements



## 🤖 AI Career Chatbot

The built-in chatbot helps users by:

- Suggesting resume improvements
- Recommending missing skills
- Giving project ideas
- Improving job readiness


## 🚀 Future Improvements
- Add login system
- Use advanced LLM (GPT / LLaMA API)
- Resume ranking system for companies
- PDF resume generator
- Job recommendation system


## 📦 Installation

- git clone https://github.com/Indrajaiswal/AI-Powered-Resume-Analyzer.git
- cd resume-analyzer
- pip install -r requirements.txt
- streamlit run app.py



## 👨‍💻 Author
Indra Jaiswal


## ⭐ If you like this project

Give it a ⭐ on GitHub and feel free to contribute!


## 📸 Project Demo

![Demo Screenshot](photos/1.png)
![Demo Screenshot](photos/2.png)
![Demo Screenshot](photos/3.png)
![Demo Screenshot](photos/4.png)
![Demo Screenshot](photos/5.png)
![Demo Screenshot](photos/6.png)


