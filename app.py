import streamlit as st
import requests
import base64
from PIL import Image
import io

OLLAMA_URL = "http://localhost:11434/api/generate"

# ------------------ Page Config ------------------
st.set_page_config(
    page_title="Engineering Analysis AI",
    page_icon="🔧",
    layout="centered"
)

st.title("🔧 Engineering Analysis AI")
st.caption("Upload your design and get expert AI-powered engineering analysis")

# ------------------ Sidebar ------------------
st.sidebar.header("⚙️ Configuration")
st.sidebar.info(
    "This app uses:\n"
    "- Moondream → Image understanding\n"
    "- TinyLlama → Engineering reasoning\n\n"
    "Optimized for low-spec laptops."
)

# ------------------ Domain Selection ------------------
domain = st.selectbox(
    "🏷️ Select the design domain",
    [
        "-- Select the domain --",
        "Robotics / Mechanical Systems",
        "Product Design",
        "CAD Model / 3D Printed",
        "Electronics / PCB Design"
    ]
)

# ------------------ Image Upload ------------------
uploaded_file = st.file_uploader(
    "📁 Upload your design image",
    type=["jpg", "jpeg", "png"]
)

user_description = st.text_area(
    "📝 Optional: Add your own notes (materials, function, concerns)",
    height=120
)

# ------------------ Helper Functions ------------------

def image_to_base64(image_file):
    image = Image.open(image_file)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()


def call_ollama(payload):
    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    return response.json()["response"]


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
