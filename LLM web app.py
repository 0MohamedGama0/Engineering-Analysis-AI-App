import streamlit as st
import requests
import io
from PIL import Image


# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="Engineering Analysis AI",
    page_icon="🔧",
    layout="centered"
)

HF_API_KEY = st.secrets.get("HF_API_KEY", None)

VISION_MODEL = "Salesforce/blip-image-captioning-base"
TEXT_MODEL = "google/flan-t5-large"

HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

# -----------------------------
# FUNCTIONS
# -----------------------------

VISION_MODEL = "Salesforce/blip-image-captioning-base"
BASE_URL = "https://router.huggingface.co/hf-inference/models"

def vision_caption(image: Image.Image) -> str:
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    response = requests.post(
        f"{BASE_URL}/{VISION_MODEL}",
        headers={
            "Authorization": f"Bearer {HF_API_KEY}",
            "Accept": "application/json"
        },
        files={"file": buffer},
        timeout=60
    )

    if response.status_code != 200:
        return f"Vision model HTTP {response.status_code}: model unavailable or loading."

    try:
        data = response.json()
    except Exception:
        return "Vision model returned invalid response."

    if isinstance(data, list) and "generated_text" in data[0]:
        return data[0]["generated_text"]

    if "error" in data:
        return f"Vision model error: {data['error']}"

    return "Unable to generate image description."

TEXT_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

def engineering_analysis(caption, user_description, domain):
    prompt = f"""
You are an expert engineering AI.

DOMAIN:
{domain}

IMAGE UNDERSTANDING (AI Vision):
{caption}

USER DESCRIPTION:
{user_description}

TASK:
Provide a structured engineering analysis including:
- System identification
- Key components
- Functionality
- Design strengths
- Weaknesses or risks
- Suggested improvements
"""

    response = requests.post(
        f"{BASE_URL}/{TEXT_MODEL}",
        headers={
            "Authorization": f"Bearer {HF_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 500,
                "temperature": 0.4
            }
        },
        timeout=60
    )

    if response.status_code != 200:
        return f"Text model HTTP {response.status_code}: model unavailable."

    try:
        data = response.json()
    except Exception:
        return "Text model returned invalid response."

    if isinstance(data, list) and "generated_text" in data[0]:
        return data[0]["generated_text"]

    if "error" in data:
        return f"Text model error: {data['error']}"

    return "Unable to generate analysis."

# -----------------------------
# UI
# -----------------------------
st.title("🔧 Engineering Analysis AI")
st.caption("Vision-Language AI for Robotics & Design Engineering")

uploaded_file = st.file_uploader(
    "Upload an engineering or design image",
    type=["png", "jpg", "jpeg"]
)

domain = st.selectbox(
    "Select domain",
    ["Robotics", "Product Design", "Mechanical", "Electronics", "CAD / 3D Printing"]
)

user_description = st.text_area(
    "Describe the design (optional but recommended)",
    height=120
)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Design", use_container_width=True)

    if st.button("Analyze Design"):
        if not HF_API_KEY:
            st.error("Hugging Face API key not found. Add it to Streamlit secrets.")
            st.stop()

        with st.spinner("Analyzing design using AI..."):
            caption = vision_caption(image)
            analysis = engineering_analysis(caption, user_description, domain)

        st.subheader("🧠 AI Image Understanding")
        st.write(caption)

        st.subheader("📊 Engineering Analysis")
        st.write(analysis)





