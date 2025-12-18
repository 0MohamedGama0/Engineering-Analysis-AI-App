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
import requests
import streamlit as st

HF_API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
HF_HEADERS = {
    "Authorization": f"Bearer {st.secrets['HF_API_KEY']}"
}

def vision_caption(image_bytes):
    response = requests.post(
        HF_API_URL,
        headers=HF_HEADERS,
        files={"file": image_bytes},
        timeout=60
    )

    # 🔴 Handle API errors safely
    if response.status_code != 200:
        raise RuntimeError(
            f"Hugging Face API error {response.status_code}: {response.text}"
        )

    try:
        data = response.json()
    except Exception:
        raise RuntimeError("Hugging Face returned non-JSON response")

    # ✅ Expected format
    if isinstance(data, list) and "generated_text" in data[0]:
        return data[0]["generated_text"]

    raise RuntimeError(f"Unexpected API response: {data}")

# ---------------- Run ----------------
if st.button("Analyze Design") and image:
    st.image(image)

    with st.spinner("Understanding image..."):
        vision_text = vision_caption(image)

    st.info(vision_text)

    with st.spinner("Performing engineering analysis..."):
        analysis = reasoning(domain, vision_text, notes)

    st.success(analysis)

