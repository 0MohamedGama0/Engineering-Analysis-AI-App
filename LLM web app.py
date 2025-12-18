import streamlit as st
import requests
from PIL import Image
import io

st.set_page_config(page_title="Engineering Analysis AI", page_icon="🔧")

st.title("🔧 Engineering Analysis AI")
st.caption("Deployed on Streamlit Cloud using Hugging Face Inference API")

# ---------------- Domain ----------------
domain = st.selectbox(
    "Select the domain",
    [
        "Robotics / Mechanical Systems",
        "Product Design",
        "CAD Model / 3D Printed",
        "Electronics / PCB Design"
    ]
)

image = st.file_uploader("Upload an engineering image", type=["jpg", "png"])
notes = st.text_area("Optional user notes")

# ---------------- Hugging Face API ----------------
HF_API_KEY = st.secrets["HF_API_KEY"]

VISION_MODEL = "Salesforce/blip-image-captioning-base"
TEXT_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

headers = {"Authorization": f"Bearer {HF_API_KEY}"}


def reasoning(domain, vision_text, notes):
    API_URL = "https://api-inference.huggingface.co/models/google/gemma-2b-it"
    headers = {
        "Authorization": f"Bearer {st.secrets['HF_API_KEY']}"
    }

    prompt = f"""
You are an expert in {domain} engineering.

IMAGE DESCRIPTION:
{vision_text}

USER NOTES:
{notes}

Provide a structured engineering analysis including:
- Technical overview
- Key components
- Design strengths
- Limitations
- Improvement suggestions
"""

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 500,
            "temperature": 0.3
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return f"❌ LLM error: {response.text}"

    try:
        data = response.json()
    except Exception:
        return "❌ Invalid response from LLM"

    if isinstance(data, list) and "generated_text" in data[0]:
        return data[0]["generated_text"]

    return "❌ Unexpected LLM output"

# ---------------- Run ----------------
if st.button("Analyze Design") and image:
    st.image(image)

    with st.spinner("Understanding image..."):
        vision_text = vision_caption(image)

    st.info(vision_text)

    with st.spinner("Performing engineering analysis..."):
        analysis = reasoning(domain, vision_text, notes)

    st.success(analysis)


