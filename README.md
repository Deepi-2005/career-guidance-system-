# 🎯 Intelligent Career Guidance System 

An intelligent, rule-based web application that offers personalized career guidance by analyzing user resumes and mapping them to relevant job roles and skill gaps. Built with **Python** and **Streamlit**, the system is lightweight, fast, and ideal for students and fresh graduates seeking direction based on their current skills.

---

## 🚀 Features

- 📄 **Resume Parsing**: Extracts key information like skills, education, and experience.
- 📊 **Resume Scoring & Skill Gap Analysis**: Evaluates your resume and suggests missing skills for targeted roles.
- 💬 **Interactive Chatbot**: Ask career-related questions and get instant, relevant responses.
- 📈 **Dashboard**: Track progress, feedback, and suggested learning paths.
- 🧪 **Recruiter Panel**: Filters and ranks resumes submitted by users.
- 🛠️ **Admin Panel**: Manage users, view feedback, and analyze usage metrics.

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit (Python)
- **Backend**: Python, TF-IDF, Cosine Similarity
- **Libraries**: 
  - `scikit-learn` – similarity analysis
  - `pandas`, `nltk` – text preprocessing
  - `re`, `string` – regex-based parsing

---

## 💡 How It Works

1. **Upload Resume** (PDF or Text)
2. **System Parses Resume**
3. **Extracted Info is Scored and Mapped**
4. **Suggestions for Skill Gap Filling are Shown**
5. **Chatbot Answers Career Questions**
6. **Dashboard Displays User Insights**

---

## 📂 Folder Structure
career-guidance-system/

│

├── app.py # Main Streamlit application

├── chatbot.py # TF-IDF based chatbot logic

├── resume_parser.py # Resume analysis and parsing

├── data/

│ ├── sample_resumes/ # Sample resume files

│ └── skills_data.csv # Job role to skills mapping

├── assets/ # Screenshots or UI assets

└── requirements.txt # Project dependencies
