# 🔧 Engineering Analysis AI — Vision-Language Web Application

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?logo=streamlit&logoColor=white)
![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Inference%20API-yellow?logo=huggingface)
![License](https://img.shields.io/badge/License-MIT-green)
![Live Demo][https://engineering-analysis-ai-web-app.streamlit.app/]. 

A professional web application for AI-powered engineering design analysis, combining computer vision and large language models. This project was created for **Assignment 4: Deploy LLM Web Applications to Streamlit Cloud** as part of the Large Language Models course.This project was created as part of a class project for the Data Science course at University of Chinese Academy of Sciences (UCAS), under the guidance of Prof. Tiejiān Luó. You can reach him at tiejianluo@gmail.com.

**Live Demo:** [https://engineering-analysis-ai.streamlit.app/](https://engineering-analysis-ai.streamlit.app/)

---

## 🎯 Overview

| Aspect | Details |
|--------|---------|
| **Course** | Large Language Models |
| **Assignment** | #4: Streamlit Cloud Deployment |
| **Student** | [MOHAMED GAMA] |
| **AI Models** | BLIP (Vision) + Mistral-7B (Text) |
| **Deployment** | Streamlit Cloud + Hugging Face Inference API |

> [!NOTE]
> This application demonstrates a complete LLM web app deployment pipeline from local development to cloud hosting with professional API integration.

---

## ✨ Features

- ✅ **Dual-Model AI Pipeline** — Computer vision + LLM for comprehensive analysis
- ✅ **Multi-Domain Engineering Analysis** — Robotics, CAD, Electronics, Product Design, etc.
- ✅ **Professional Interface** — Clean, responsive Streamlit UI with custom CSS
- ✅ **Robust Error Handling** — Graceful fallbacks for API failures
- ✅ **Secure API Integration** — Hugging Face Inference API with secret management
- ✅ **Export Capability** — Download analysis reports as text files
- ✅ **Demo Mode** — Functional interface without API key requirements

---

### 🏗️ Architecture
```
┌─────────────────────────────────────────────┐
│ Streamlit UI Layer                          │
│ ┌──────────────────────────────────────┐    │
│ │ Image Upload | Domain Selection      │    │
│ │ Description Input | Analysis Display │    │
│ └──────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
↓
┌─────────────────────────────────────────────┐
│ Hugging Face API Gateway                    │
│ ┌──────────────────────────────────────┐    │
│ │ Vision Model (BLIP)                  │    │
│ │ Text Model (Mistral-7B-Instruct)     │    │
│ │ Authentication & Rate Limiting       │    │
│ └──────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
↓
┌─────────────────────────────────────────────┐
│ Analysis Engine                             │
│ ┌──────────────────────────────────────┐    │
│ │ Prompt Engineering                   │    │
│ │ Domain-Specific Templates            │    │
│ │ Response Formatting                  │    │
│ └──────────────────────────────────────┘    │
└─────────────────────────────────────────────┘

```

---

## 🚀 Quick Deployment

### Prerequisites

- Python 3.8 or higher
- Git installed
- Hugging Face account (for full functionality)
- Streamlit Cloud account

### Local Development

1. **Clone and setup:**
   ```bash
   git clone https://github.com/yourusername/engineering-analysis-ai.git
   cd engineering-analysis-ai
   
   # Create virtual environment
   python -m venv .venv
   
   # Activate (Windows)
   .venv\Scripts\activate
   
   # Activate (macOS/Linux)
   source .venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt



   # Create secrets file
   mkdir .streamlit
   echo 'HF_API_KEY = "your_huggingface_token_here"' > .streamlit/secrets.toml

##Streamlit Cloud Deployment
##Push to GitHub:
  git add .
  git commit -m "Deploy Engineering Analysis AI"
  git push origin main


##📁 Project Structure
```
engineering-analysis-ai/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # This documentation
├── .streamlit/
│   ├── secrets.toml           # API key configuration
│   └── config.toml            # Streamlit settings
└── assets/                    # Screenshots and resources
    ├── screenshot-1.png
    └── architecture.png
```

Process Description:

text
1. Local Development Phase (4 hours)
   - Created HTML/JavaScript version with Ollama
   - Tested with TinyLlama model
   - Implemented image upload and description

2. Cloud Adaptation Phase (3 hours)
   - Converted to Streamlit Python app
   - Integrated Hugging Face Inference API
   - Added professional UI with custom CSS

3. Deployment Phase (2 hours)
   - Created GitHub repository
   - Configured Streamlit Cloud deployment
   - Set up API key management with secrets

4. Testing & Documentation (3 hours)
   - Tested both demo and full API modes
   - Created professional README.md
   - Prepared assignment report
  


📧 Contact
Student: [Mohamed Ishag Hassan]
Course: ISE- UCAS
Assignment: #4 - Streamlit Cloud Deployment

Live App: https://engineering-analysis-ai.streamlit.app/
GitHub: https://github.com/yourusername/engineering-analysis-ai

Built with Passion for innovators

## Keep moving forward 
