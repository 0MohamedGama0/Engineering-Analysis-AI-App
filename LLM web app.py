import streamlit as st
import requests
import base64
from PIL import Image
import io
import os

HF_API_KEY = st.secrets["HF_API_KEY"]
HF_MODEL = "Salesforce/blip-image-captioning-base"
HF_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

st.set_page_config(page_title="Engineering Analysis AI", layout="centered")

st.title("🔧 Engineering Analysis AI")
st.write("Upload an engineering or robotics design image for AI analysis")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

def analyze_image(image_bytes):
    response = requests.post(
        HF_URL,
        headers=headers,
        files={"file": image_bytes}
    )

    if response.status_code != 200:
        st.error("Hugging Face API error")
        return None

    return response.json()

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Design", use_column_width=True)

    if st.button("Analyze Design"):
        with st.spinner("Analyzing with AI..."):
            result = analyze_image(uploaded_file.getvalue())

        if result:
            caption = result[0]["generated_text"]
            st.subheader("🧠 AI Interpretation")
            st.write(caption)

            st.subheader("🔍 Engineering Insight")
            st.write(f"""
            This design appears to involve **{caption.lower()}**.

            From an engineering perspective, this system likely involves:
            - Mechanical structure and load-bearing components
            - Actuation and motion control
            - Potential integration with sensors or electronics
            - Design-for-manufacturing considerations
            """)

def vision_analysis(image_b64):
    payload = {
        "model": "moondream",
        "prompt": "Describe this engineering image clearly and objectively.",
        "images": [image_b64],
        "stream": False
    }
    return call_ollama(payload)


def engineering_analysis(domain, vision_text, user_text):
    prompt = f"""
You are an expert engineering analyst.

IMAGE INTERPRETATION (AI Vision):
{vision_text}

USER NOTES:
{user_text if user_text else "No additional notes provided."}

TASK:
1. Validate the image interpretation
2. Correct inconsistencies if any
3. Provide structured, domain-specific engineering analysis
4. Identify risks and improvements

DOMAIN:
{domain}

Respond professionally and clearly.
"""
    payload = {
        "model": "tinyllama:latest",
        "prompt": prompt,
        "stream": False
    }
    return call_ollama(payload)


# ------------------ Run Analysis ------------------
if st.button("🚀 Analyze Design", disabled=not (uploaded_file and domain != "-- Select the domain --")):

    st.subheader("📷 Uploaded Image")
    st.image(uploaded_file, use_column_width=True)

    with st.spinner("🔍 Understanding image..."):
        image_b64 = image_to_base64(uploaded_file)
        vision_result = vision_analysis(image_b64)

    st.subheader("🧠 AI Image Interpretation")
    st.info(vision_result)

    with st.spinner("⚙️ Performing engineering analysis..."):
        analysis_result = engineering_analysis(domain, vision_result, user_description)

    st.subheader("📊 Engineering Analysis Result")
    st.success(analysis_result)

