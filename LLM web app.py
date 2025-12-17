import streamlit as st
import requests

# ---------------- CONFIG ----------------
HF_API_URL = "https://router.huggingface.co/hf-inference/models/google/gemma-2b-it"
HF_API_KEY = st.secrets["HF_API_KEY"]

HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

# ---------------- FUNCTIONS ----------------
def call_llm(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 400,
            "temperature": 0.4
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

    return response.json()[0]["generated_text"]

# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="Engineering Analysis AI", layout="centered")

st.title("🔧 Engineering Analysis AI")
st.caption("LLM-Based Design Reasoning for Robotics & Engineering")

uploaded_image = st.file_uploader(
    "Upload an engineering-related image",
    type=["png", "jpg", "jpeg"]
)

domain = st.selectbox(
    "Select domain",
    [
        "Robotics / Mechanical Systems",
        "Product Design",
        "CAD Model / 3D Printed",
        "Electronics / PCB Design"
    ]
)

description = st.text_area(
    "Describe what you see in the image",
    placeholder="Example: robotic arm with servo motors and aluminum links"
)

if uploaded_image:
    st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

if st.button("Analyze Design"):
    if not description:
        st.warning("Please provide a brief description.")
    else:
        with st.spinner("Analyzing design using AI..."):
            prompt = f"""
You are an engineering expert.

Domain: {domain}

User description of the image:
{description}

Provide:
1. Functional interpretation
2. Key components
3. Engineering considerations
4. Possible improvements
"""

            result = call_llm(prompt)

        st.success("Analysis Complete")
        st.markdown(result)
