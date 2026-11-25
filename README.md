# 🤖 Agentic AI Career Copilot

An AI-powered career assistance application that analyzes resumes against job descriptions, identifies skill gaps, and generates personalized learning recommendations using Google Gemini.

## 🚀 Project Overview

Agentic AI Career Copilot helps students and job seekers understand their job readiness. Users can upload a resume in PDF format and provide a job description to receive AI-powered career insights.

This project explores how Large Language Models (LLMs), Python tools, and function calling can work together to build practical AI applications.

## ✨ Features

- **Resume PDF Extraction:** Extracts text from uploaded resumes.
- **Skill Matching:** Compares resume skills against job requirements.
- **AI Career Analysis:** Uses Google Gemini to analyze job fit.
- **Missing Skill Identification:** Highlights skills that need improvement.
- **Personalized Learning Plan:** Uses Python tool calling to generate learning topics for missing skills.

## 🛠️ Technology Stack

- Python
- Streamlit
- Google Gemini API
- Google GenAI SDK
- PyPDF
- Jupyter Notebook
- Visual Studio Code

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Agentic-AI-Career-Copilot
```

### 2. Install dependencies

```bash
pip install streamlit pypdf google-genai
```

### 3. Configure your Gemini API key

Create a folder named `.streamlit` in the project directory.

Inside it, create a file named `secrets.toml`:

```toml
GOOGLE_API_KEY = "YOUR_GEMINI_API_KEY"
```

Replace the placeholder with your own Gemini API key.

**Important:** Never upload `secrets.toml` or share your API key publicly.

### 4. Run the application

```bash
python -m streamlit run app.py
```

## 📌 Current Development Status

- [x] Streamlit application setup
- [x] Resume PDF text extraction
- [x] Basic skill matching
- [x] Google Gemini integration
- [x] AI-powered career analysis
- [x] Python tool calling
- [x] Personalized learning plan
- [ ] AI-powered mock interview system
- [ ] Interview answer evaluation and feedback
- [ ] Final testing and UI improvements

## 🎯 Project Goal

To develop an intelligent career assistant that helps candidates evaluate their job readiness and improve their skills through personalized AI-powered guidance.

## 👩‍💻 Author

Developed as a final-year academic project while exploring Generative AI and Agentic AI.

**Currently learning and building in the field of Artificial Intelligence.**