# 🎓 AI Career Path Guide — Team 46Dubey

This web application recommends career paths using AI (OpenAI + Gemini).
Users enter their education, interests, and goals, and the app generates
a full personalized roadmap with motivation guidance.

---

## Problem Statement

1. Many graduates struggle to identify courses aligned with their career goals.
2. Lack of guidance leads to confusion and delays in starting careers.

---

### 🚀 Live Demo
🔗 Deployed on Streamlit Cloud  
([Click to open Link](https://nxtwave-pulkitdubey.streamlit.app/))

---

## ✨ Features
- Personalized AI Career Recommendations
- Government & Private Job Guidance
- Courses & Skill Roadmap
- Motivational Insights Powered by Gemini
- Clean UI with Restart Option

---

## 🛠 Tech Stack
| Component | Technology |
|----------|------------|
| Frontend | Streamlit |
| AI Models | OpenAI GPT-4.1 Mini + Gemini 2.5 Flash |
| Language | Python |

---

## 🔑 Environment Variables

Add these as **Secrets** in Streamlit Cloud:
```bash
OPENAI_API_KEY = "your_openai_key"
GOOGLE_API_KEY = "your_gemini_key"
```
---

## ▶ Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📌 Author

👨‍💻 Developed by Pulkit Dubey (Team 46Dubey)

Made with ❤️ during Buildathon (22 Nov - 23 Nov)
