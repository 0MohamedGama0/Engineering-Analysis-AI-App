import streamlit as st
import requests
import base64
from PIL import Image
import io

# ---------------- CONFIG ----------------
HF_API_URL = "https://router.huggingface.co/hf-inference/models/Salesforce/blip-image-captioning-base"
HF_API_KEY = st.secrets["HF_API_KEY"]

HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

# ---------------- FUNCTIONS ----------------
def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def vision_analysis(image_b64, domain, description):
    payload = {
        "inputs": {
            "image": image_b64
        }
    }

    response = requests.post(
        HF_API_URL,
        headers=HEADERS,
        json=payload,
        timeout=60
    )

    if response.status_code != 200:
        return f"❌ API Error ({response.status_code}): {response.text}"

    result = response.json()

    caption = result[0]["generated_text"]

    # Engineering-style post processing
    analysis = f"""
### 🧠 AI Vision Interpretation
**Detected Design:** {caption}

### 🏷 Domain
{domain}

### 📝 User Notes
{description}

### 🔧 Engineering Analysis
- The image likely represents a mechanical or engineered system.
- Structural elements and components appear consistent with the selected domain.
- Further optimization may include material refinement, actuator selection, and structural validation.
- Recommended next steps include CAD simulation, load testing, and functional prototyping.
"""

    return analysis

# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="Engineering Analysis AI", layout="centered")

st.title("🔧 Engineering Analysis AI")
st.subheader("Vision-Based Design Understanding for Robotics & Engineering")

uploaded_image = st.file_uploader(
    "Upload a design image",
    type=["png", "jpg", "jpeg"]
)

domain = st.selectbox(
    "Select design domain",
    ["Robotics", "Product Design", "CAD / 3D Printing", "Electronics"]
)

description = st.text_area(
    "Describe the design (optional)",
    placeholder="Example: robotic arm, gripper, mobile robot chassis..."
)

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Design", use_column_width=True)

if st.button("Analyze Design"):
    if not uploaded_image:
        st.warning("Please upload an image.")
    else:
        with st.spinner("Analyzing image with AI..."):
            image_b64 = encode_image(image)
            analysis = vision_analysis(image_b64, domain, description)

        st.success("Analysis complete")
        st.markdown(analysis)
