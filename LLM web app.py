import streamlit as st
import io
from PIL import Image
from huggingface_hub import InferenceClient

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="Engineering Analysis AI",
    page_icon="🔧",
    layout="centered"
)

# Get API key from Streamlit secrets
HF_API_KEY = st.secrets.get("HF_API_KEY", None)

# Initialize the clients
vision_client = InferenceClient(token=HF_API_KEY)
text_client = InferenceClient(token=HF_API_KEY)

# -----------------------------
# FUNCTIONS
# -----------------------------

def vision_caption(image: Image.Image) -> str:
    """Generate a caption for the uploaded image."""
    try:
        # The client handles the image conversion and API call
        result = vision_client.image_to_text(image=image)
        return result
    except Exception as e:
        return f"Vision model error: {str(e)}"

def engineering_analysis(caption, user_description, domain):
    """Generate engineering analysis based on image caption and user description."""
    prompt = f"""
You are an expert engineering AI.

DOMAIN:
{domain}

IMAGE UNDERSTANDING (AI Vision):
{caption}

USER DESCRIPTION:
{user_description if user_description else "No additional description provided by user."}

TASK:
Provide a structured engineering analysis including:
- System identification
- Key components
- Functionality
- Design strengths
- Weaknesses or risks
- Suggested improvements

Keep the analysis concise, technical, and focused on the {domain} domain.
"""
    
    try:
        # Use the text client for text generation
        result = text_client.text_generation(
            prompt=prompt,
            max_new_tokens=500,
            temperature=0.4
        )
        return result
    except Exception as e:
        return f"Text model error: {str(e)}"

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
    height=120,
    placeholder="Example: 'This is a robotic arm prototype with 4 degrees of freedom...'"
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
