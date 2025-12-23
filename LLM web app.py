import streamlit as st
import requests
import base64
from PIL import Image
import io

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Engineering Analysis AI",
    page_icon="🔧",
    layout="wide"
)

# --------------------------------------------------
# Constants & Models
# --------------------------------------------------
BASE_URL = "https://router.huggingface.co/hf-inference/models"

VISION_MODEL = "qwen/qwen-2.5-vl-7b-instruct:free"
TEXT_MODEL = "xiaomi/mimo-v2-flash:free"

HF_API_KEY = st.secrets.get("HF_API_KEY")
if not HF_API_KEY:
    st.error("HF_API_KEY is missing. Please add it in Streamlit Secrets.")
    st.stop()

HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

# --------------------------------------------------
# Session State
# --------------------------------------------------
if "vl_failed" not in st.session_state:
    st.session_state.vl_failed = False

if "vision_result" not in st.session_state:
    st.session_state.vision_result = ""

if "final_analysis" not in st.session_state:
    st.session_state.final_analysis = ""

# --------------------------------------------------
# Helper Functions
# --------------------------------------------------
def image_to_base64(image: Image.Image) -> str:
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def vision_language_analysis(image: Image.Image) -> str:
    """Primary Vision-Language model call"""
    img_b64 = image_to_base64(image)

    payload = {
        "inputs": [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": img_b64},
                    {"type": "text", "text": "Describe the engineering object or system in this image."}
                ]
            }
        ]
    }

    response = requests.post(
        f"{BASE_URL}/{VISION_MODEL}",
        headers={**HEADERS, "Content-Type": "application/json"},
        json=payload,
        timeout=90
    )

    if response.status_code != 200:
        return "VISION_ERROR"

    try:
        data = response.json()
    except Exception:
        return "VISION_ERROR"

    try:
        return data["choices"][0]["message"]["content"]
    except Exception:
        return "VISION_ERROR"


def text_only_analysis(text_input: str, domain: str) -> str:
    """Fallback Text-only analysis"""
    prompt = f"""
You are an expert engineering analyst.

DOMAIN:
{domain}

INPUT DESCRIPTION:
{text_input}

TASK:
Provide a structured engineering analysis including:
- Identification of the system or object
- Key components
- Functionality
- Design strengths
- Limitations or risks
- Suggested improvements
"""

    response = requests.post(
        f"{BASE_URL}/{TEXT_MODEL}",
        headers={**HEADERS, "Content-Type": "application/json"},
        json={
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 500,
                "temperature": 0.4
            }
        },
        timeout=90
    )

    if response.status_code != 200:
        return "TEXT_ERROR"

    try:
        data = response.json()
    except Exception:
        return "TEXT_ERROR"

    if isinstance(data, list) and "generated_text" in data[0]:
        return data[0]["generated_text"]

    if "generated_text" in data:
        return data["generated_text"]

    return "TEXT_ERROR"

# --------------------------------------------------
# UI Layout
# --------------------------------------------------
st.title("🔧 Engineering Analysis AI")
st.caption("Vision–Language Engineering Analysis with Robust Fallback")

left, right = st.columns(2)

# --------------------------------------------------
# Left Column: Inputs
# --------------------------------------------------
with left:
    st.subheader("Input")

    uploaded_file = st.file_uploader(
        "Upload an engineering-related image (JPG / PNG)",
        type=["jpg", "jpeg", "png"]
    )

    domain = st.selectbox(
        "Select the domain",
        [
            "Robotics / Mechanical Systems",
            "Product Design",
            "CAD Model / 3D Printed",
            "Electronics / PCB Design"
        ]
    )

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", height=260)

        if st.button("Analyze Image"):
            with st.spinner("Running vision-language analysis..."):
                result = vision_language_analysis(image)

            if result == "VISION_ERROR":
                st.session_state.vl_failed = True
                st.warning(
                    "Vision model is temporarily unavailable.\n"
                    "Please enter a short description manually."
                )
            else:
                st.session_state.vision_result = result
                st.session_state.vl_failed = False

    if st.session_state.vl_failed:
        manual_input = st.text_input(
            "Manual description (fallback mode)",
            placeholder="Example: robotic arm with 4 DOF and gripper"
        )

        if st.button("Analyze via Text Model"):
            with st.spinner("Running text-only analysis..."):
                st.session_state.final_analysis = text_only_analysis(
                    manual_input, domain
                )

# --------------------------------------------------
# Right Column: Results
# --------------------------------------------------
with right:
    st.subheader("Results")

    if st.session_state.vision_result:
        st.markdown("### 🧠 AI Image Understanding")
        st.write(st.session_state.vision_result)

        if st.button("Generate Engineering Analysis"):
            with st.spinner("Generating engineering analysis..."):
                st.session_state.final_analysis = text_only_analysis(
                    st.session_state.vision_result, domain
                )

    if st.session_state.final_analysis:
        st.markdown("### 📊 Engineering Analysis")
        st.write(st.session_state.final_analysis)
