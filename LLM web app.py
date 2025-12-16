import streamlit as st
import requests
import base64

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Engineering Analysis AI",
    page_icon="🔧",
    layout="centered"
)

HF_API_KEY = st.secrets["HF_API_KEY"]
MODEL_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

# ---------------- UI ----------------
st.title("🔧 Engineering Analysis AI")
st.caption("Robotics • Design Engineering • Startups")

image = st.file_uploader(
    "Upload your design image (for reference)",
    type=["png", "jpg", "jpeg"]
)

domain = st.selectbox(
    "Select design domain",
    [
        "Robotics / Mechanical Systems",
        "Product Design",
        "CAD / 3D Printing",
        "Electronics / PCB Design"
    ]
)

description = st.text_area(
    "Describe what you see in the image",
    placeholder="Example: A 4-DOF robotic arm using servo motors and aluminum links..."
)

analyze = st.button("Analyze Design")

# ---------------- PROMPT ----------------
def build_prompt(domain, description):
    return f"""
You are a professional engineering expert.

Domain: {domain}

Design description:
{description}

Provide a structured engineering analysis including:
- Technical overview
- Key components
- Strengths and weaknesses
- Design improvements
- Real-world applications
"""

# ---------------- LLM CALL ----------------
def call_llm(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.5,
            "max_new_tokens": 400
        }
    }

    response = requests.post(
        MODEL_URL,
        headers=HEADERS,
        json=payload,
        timeout=60
    )

    if response.status_code != 200:
        st.error(f"Model error: {response.text}")
        return None

    try:
        data = response.json()
        return data[0]["generated_text"]
    except Exception:
        st.error("Failed to parse model response.")
        st.text(response.text)
        return None

# ---------------- EXECUTION ----------------
if analyze:
    if not description:
        st.warning("Please describe the design.")
    else:
        with st.spinner("Analyzing design..."):
            prompt = build_prompt(domain, description)
            result = call_llm(prompt)

        if result:
            st.success("Analysis complete")
            st.markdown(result)
