# 🔧 Engineering Analysis AI — Vision-Language Web Application

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red?logo=streamlit&logoColor=white)
![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Inference%20Providers-yellow?logo=huggingface)
![OpenAI SDK](https://img.shields.io/badge/OpenAI%20SDK-Compatible-green)
![License](https://img.shields.io/badge/License-MIT-green)

A professional web application for **AI-powered engineering design analysis**, combining advanced **vision-language models** with structured LLM reasoning. This project was created as part of a **Data Science / Large Language Models course assignment** at the University of Chinese Academy of Sciences (UCAS), under the guidance of Prof. Tiejiān Luó (tiejianluo@gmail.com).

**Live Demo:** [https://engineering-analysis-ai.streamlit.app/](https://engineering-analysis-ai.streamlit.app/)

**GitHub Repository:** [https://github.com/0MohamedGama0/engineering-analysis-ai-web-app](https://github.com/0MohamedGama0/engineering-analysis-ai-web-app) (replace with your actual repo URL)

---

## 🎯 Overview

| Aspect              | Details                                      |
|---------------------|----------------------------------------------|
| **Language**        | Python 3.10+                                 |
| **Framework**       | Streamlit                                    |
| **Vision Model**    | Qwen/Qwen2.5-VL-7B-Instruct                   |
| **Text Model**      | meta-llama/Meta-Llama-3.1-8B-Instruct         |
| **Deployment**      | Streamlit Community Cloud                    |
| **Inference API**   | Hugging Face Inference Providers (OpenAI-compatible router) |

> This application implements a robust **vision–language pipeline**: an uploaded engineering image is analyzed by a powerful vision-language model for detailed technical description, followed by structured engineering analysis using a strong text LLM, with domain-specific prompting and graceful fallback.

---

## ✨ Features

- 🖼️ Image upload (JPG/PNG) for CAD models, robotics, PCBs, product designs, etc.
- 🧠 Advanced AI image understanding via modern Vision-Language Model
- 📊 Structured engineering analysis (identification, components, functionality, strengths, risks, improvements)
- 🏷️ Domain-specific analysis options:
  - Robotics / Mechanical Systems
  - Product Design
  - CAD Model / 3D Printed
  - Electronics / PCB Design
- ⚠️ Robust fallback to manual text description if vision model temporarily unavailable
- 🔐 Secure handling of Hugging Face API key via Streamlit Secrets
- ☁️ Fully deployed and free to use on Streamlit Cloud

---

## 🚀 How It Works

1. User uploads an engineering-related image and selects a domain.
2. Vision-Language Model (Qwen2.5-VL-7B) generates a detailed technical description of the object/system.
3. Text LLM (Llama-3.1-8B-Instruct) uses the description + domain to produce a structured engineering analysis.
4. If the vision step fails (rate limits, temporary outage), user can manually enter a description as fallback.

---

## 🛠️ Installation (Local Development)

### Prerequisites
- Python 3.10+
- Git
- Hugging Face account & API token (free tier works for testing)

### Steps


git clone https://github.com/0MohamedGama0/engineering-analysis-ai-web-app.git
cd engineering-analysis-ai-web-app
pip install -r requirements.txt

# Create local secrets (do NOT commit this file)
mkdir .streamlit
echo 'HF_API_KEY = "hf_your_token_here"' > .streamlit/secrets.toml

streamlit run app.py

### 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│ Streamlit UI Layer                          │
│ • Image Upload                              │
│ • Domain Selection                          │
│ • Vision Analysis Button                    │
│ • Fallback Manual Input                     │
│ • Results Display                           │
└─────────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────┐
│ Hugging Face Inference Providers (Router)   │
│ • OpenAI-compatible endpoint                │
│   https://router.huggingface.co/v1          │
│ • Vision: Qwen/Qwen2.5-VL-7B-Instruct       │
│ • Text:meta-llama/Meta-Llama-3.1-8B-Instruct│
└─────────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────┐
│ Analysis Engine                             │
│ • Detailed technical description prompt     │
│ • Structured engineering analysis template  │
│ • Error handling & fallback logic           │
└─────────────────────────────────────────────┘

```

### ☁️ Deployment to Streamlit Cloud
---
 - Push your code to GitHub (ensure .streamlit/secrets.toml is in .gitignore)
 - Go to https://share.streamlit.io
 - New app → Select your repository → Branch: main → Main file: app.py
 - In Advanced settings → Secrets → Add:textHF_API_KEY = "hf_your_actual_token_here
---

## 📁 Project Structure

---

engineering-analysis-ai-web-app/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Dependencies
├── README.md               # This file
└── .streamlit/
    └── secrets.toml        # API keys (local only – NOT committed to GitHub)

    

### 📦 Dependencies (requirements.txt)

```bash

streamlit
pillow
openai>=1.0.0

---


##  🐞 Development Challenges & Solutions

```bash

Problem,Solution
Initial code used outdated direct model endpoints (:free suffix),Migrated to modern Hugging Face Inference Providers with OpenAI-compatible router
"Vision model calls failing (wrong payload format, unsupported task)","Switched to openai Python client with base_url=""https://router.huggingface.co/v1"" and proper chat format with base64 data URI"
"Text model errors (""model not supported for task text-generation"")",Used chat completion models only (Llama-3.1-8B-Instruct) via OpenAI-style messages
Older models like BLIP/FLAN-T5/Mistral-7B unavailable or unreliable on free tier,Upgraded to current strong open models: Qwen2.5-VL-7B-Instruct (vision) and Meta-Llama-3.1-8B-Instruct (text)
Local Ollama worked but incompatible with cloud deployment,Fully replaced with cloud-based Hugging Face Inference (no local dependencies)
Rate limits / temporary model unavailability,"Added robust error handling, user feedback, and manual description fallback"
UI confusion during errors,"Improved buttons, success/error messages, and layout for better UX"


## Built with passion for engineering innovation 🚀
Keep Moving Forward
Student: Mohamed Gama
Course: Data Science / Large Language Models – UCAS
## 📄 License
MIT License — free for academic, educational, and personal use.
