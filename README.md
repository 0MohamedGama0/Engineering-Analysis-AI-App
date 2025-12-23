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
|------|--------|
| **Language** | Python 3.9+ |
| **Framework** | Streamlit |
| **Vision Model** | BLIP (Image Captioning) |
| **Text Model** | FLAN-T5 |
| **Deployment** | Streamlit Cloud |
| **Inference API** | Hugging Face Router |

> This application demonstrates a **vision–language pipeline** where an uploaded image is first interpreted by an AI vision model and then analyzed using a text-based LLM.

---

## ✨ Features

- 🖼️ Image upload (CAD, robotics, electronics, product designs)
- 🧠 AI image understanding (vision model)
- 📊 Engineering analysis using LLM reasoning
- 🏷️ Domain-specific analysis:
  - Robotics / Mechanical Systems
  - Product Design
  - CAD / 3D Printed Models
  - Electronics / PCB Design
- ☁️ Fully deployed on Streamlit Cloud
- 🔐 Secure API key handling via Streamlit Secrets


## 🚀 How It Works

---

## 🛠️ Installation (Local)

### Prerequisites
- Python 3.9+
- pip

### Steps

```
bash
git clone https://github.com/0MohamedGama0/engineering-analysis-ai-web-app.git
cd engineering-analysis-ai-web-app
pip install -r requirements.txt
streamlit run app.py

```
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


## 🚀 Quick Deployment

### Prerequisites

- Python 3.8 or higher
- Git installed
- Hugging Face account (for full functionality)
- Streamlit Cloud account

### Local Development

1. **Clone and setup:**
   ```bash
   git clone https://github.com/0MohamedGama0/engineering-analysis-ai.git
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

## ☁️ Deployment (Streamlit Cloud)
## Push to GitHub:
  git add .
  git commit -m "Deploy Engineering Analysis AI"
  git push origin main
 
  Push code to GitHub
  Go to https://streamlit.io/cloud
  Click New App
  Select repository & app.py
  Add secret: HF_API_KEY = your_huggingface_api_key


## 📁 Project Structure
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

## 📦 Dependencies
```
  streamlit
  requests
  pillow
```


## 📄 License
```
MIT License — free for academic and educational use.
# ✅ 3. GitHub Repository Structure
Your repo **must look like this**:

engineering-analysis-ai-web-app/
│
├── app.py
├── requirements.txt
├── README.md
└── .streamlit/
└── secrets.toml (local only, NOT pushed)

```


### Process Description:

text
1. Local Development Phase (4 hours)
   - Created HTML/JavaScript version with Ollama
   - Tested with TinyLlama model
   - Implemented image upload and description

2. Cloud Adaptation Phase (8 hours)
   - Converted to Streamlit Python app
   - Integrated Hugging Face Inference API
   - Added professional UI with custom CSS

3. Deployment Phase (2 hours)
   - Created GitHub repository
   - Configured Streamlit Cloud deployment
   - Set up API key management with secrets

4. Testing & Documentation (4 hours)
   - Tested both demo and full API modes
   - Created professional README.md
   - Prepared assignment report

---

# ✅ 4. Implementation Documentation (FOR THE PDF)

### 🔧 Process Description
> The application was developed using Streamlit and deployed on Streamlit Cloud. A vision-language pipeline was implemented where uploaded images are first processed by a vision model to generate captions, which are then combined with user input and domain selection to produce an engineering analysis using a text-based large language model.

### ⏱️ Total Time Spent
> Approximately **10–12 hours**, including development, debugging, deployment, and documentation.

### 🐞 Problems Encountered & Solutions

| Problem | Solution |
|------|---------|
| Hugging Face API deprecated | Migrated to `router.huggingface.co` |
| Vision model unavailable | Switched to lightweight BLIP model |
| Ollama incompatible with cloud | Replaced with cloud inference |
| HTTP 404/410 errors | Used router-supported models |
| Streamlit secrets error | Configured secrets properly |

### 💡 Helpful Hints for Others
- Use **lightweight models** for Streamlit Cloud
- Always handle API failures gracefully
- Avoid local-only tools (e.g., Ollama) for cloud deployment
- Test deployment twice due to model cold starts

---

📧 Contact
Student: [Mohamed Gama]
Course: ISE- UCAS
Assignment: #4 - Streamlit Cloud Deployment

Live App: [https://engineering-analysis-ai.streamlit.app/](https://engineering-analysis-ai-web-app.streamlit.app/)
GitHub: https://github.com/yourusername/engineering-analysis-ai

Built with Passion for innovators

## Keep Moving Forward 
