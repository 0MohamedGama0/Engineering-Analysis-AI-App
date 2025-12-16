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


API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
HEADERS = {
    "Authorization": f"Bearer {st.secrets['HF_API_KEY']}"
}

def vision_caption(image):
    response = requests.post(
        API_URL,
        headers=HEADERS,
        files={"image": image}
    )

    # 🔴 SAFETY CHECK
    if response.status_code != 200:
        st.error("Hugging Face API Error")
        st.write(response.text)
        return "Error analyzing image."

    try:
        data = response.json()
        return data[0]["generated_text"]
    except Exception:
        st.error("Invalid API response")
        st.write(response.text)
        return "Model response error."


# ---------------- Run ----------------
if st.button("Analyze Design") and image:
    st.image(image)

    with st.spinner("Understanding image..."):
        vision_text = vision_caption(image)

    st.info(vision_text)

    with st.spinner("Performing engineering analysis..."):
        analysis = reasoning(domain, vision_text, notes)

    st.success(analysis)

