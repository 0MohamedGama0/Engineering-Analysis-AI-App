import streamlit as st
import requests
from PIL import Image
import io

# ------------------------------
# CONFIG
# ------------------------------
st.set_page_config(
    page_title="Engineering Analysis AI",
    page_icon="🔧",
    layout="centered"
)

HF_API_KEY = st.secrets["HF_API_KEY"]

VISION_MODEL = "Salesforce/blip-image-captioning-large"
TEXT_MODEL = "google/gemma-2b-it"

HF_ROUTER = "https://router.huggingface.co/hf-inference/models/"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

# ------------------------------
# FUNCTIONS
# ------------------------------

def vision_caption(image):
    url = HF_ROUTER + VISION_MODEL

    img_bytes = io.BytesIO()
    image.save(img_bytes, format="PNG")
    img_bytes = img_bytes.getvalue()

    response = requests.post(
        url,
        headers=headers,
        data=img_bytes,
        timeout=60
    )

    if response.status_code != 200:
        st.error(response.text)
        return None

    return response.json()[0]["generated_text"]


def engineering_analysis(caption, domain):
    url = HF_ROUTER + TEXT_MODEL

    prompt = f"""
You are an expert {domain} engineer.

Analyze the following design described from an image:

"{caption}"

Provide:
1. Technical overview
2. Key components
3. Engineering strengths
4. Limitations
5. Improvement suggestions
"""

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 400
        }
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=60
    )

    if response.status_code != 200:
        st.error(response.text)
        return None

    return response.json()[0]["generated_text"]

# ------------------------------
# UI
# ------------------------------

st.title("🔧 Engineering Analysis AI")
st.caption("Vision-Language LLM for Robotics, Design & Engineering")

uploaded_image = st.file_uploader(
    "Upload an engineering image (robot, CAD, mechanism)",
    type=["png", "jpg", "jpeg"]
)

domain = st.selectbox(
    "Select domain",
    ["Robotics", "Mechanical Design", "Product Design", "Electronics"]
)

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    if st.button("Analyze Design"):
        with st.spinner("Analyzing image..."):
            caption = vision_caption(image)

        if caption:
            st.success("Image understood successfully!")
            st.write("**Image Description:**")
            st.write(caption)

            with st.spinner("Generating engineering analysis..."):
                analysis = engineering_analysis(caption, domain)

            if analysis:
                st.subheader("🔍 Engineering Analysis")
                st.write(analysis)
