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
def vision_caption(image):
    API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
    headers = {
        "Authorization": f"Bearer {st.secrets['HF_API_KEY']}"
    }

    response = requests.post(
        API_URL,
        headers=headers,
        files={"image": image}
    )

    # 🔍 DEBUG: check response status
    if response.status_code != 200:
        st.error(f"Hugging Face API Error: {response.status_code}")
        st.code(response.text)
        return "❌ Model error"

    # 🔍 Try parsing JSON safely
    try:
        data = response.json()
    except Exception:
        st.error("Invalid response from Hugging Face")
        st.code(response.text)
        return "❌ Invalid API response"

    # 🔍 Handle model loading
    if isinstance(data, dict) and "error" in data:
        if "loading" in data["error"].lower():
            return "⏳ Model is loading, please try again in 20–30 seconds."
        return f"❌ API Error: {data['error']}"

    # 🔍 Expected successful response
    if isinstance(data, list) and "generated_text" in data[0]:
        return data[0]["generated_text"]

    return "❌ Unexpected API response format"

# =============================
# 2️⃣ STREAMLIT UI
# =============================

st.set_page_config(page_title="Engineering Analysis AI")

st.title("🔧 Engineering Analysis AI")

uploaded_file = st.file_uploader("Upload an engineering image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    if st.button("Analyze Image"):
        with st.spinner("Analyzing..."):
            vision_text = vision_caption(uploaded_file)
            st.success("Analysis Complete")
            st.write(vision_text)

# ---------------- Run ----------------
if st.button("Analyze Design") and image:
    st.image(image)

    with st.spinner("Understanding image..."):
        vision_text = vision_caption(image)

    st.info(vision_text)

    with st.spinner("Performing engineering analysis..."):
        analysis = reasoning(domain, vision_text, notes)

    st.success(analysis)






