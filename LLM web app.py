import streamlit as st
from huggingface_hub import InferenceClient
import os

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Engineering Analysis AI",
    page_icon="🔧",
    layout="centered"
)

# Get your Hugging Face API key from Streamlit secrets
HF_TOKEN = st.secrets.get("HF_API_KEY", os.getenv("HF_API_KEY"))

# Initialize the InferenceClient with the new API
client = InferenceClient(token=HF_TOKEN)

# ---------------- UI ----------------
st.title("🔧 Engineering Analysis AI")
st.caption("Robotics • Design Engineering • Startups")

image = st.file_uploader(
    "Upload your design image (for reference)",
    type=["png", "jpg", "jpeg"]
)

domain = st.selectbox(
    "Select design domain",
    [
        "Robotics / Mechanical Systems",
        "Product Design",
        "CAD / 3D Printing",
        "Electronics / PCB Design"
    ]
)

description = st.text_area(
    "Describe what you see in the image",
    placeholder="Example: A 4-DOF robotic arm using servo motors and aluminum links..."
)

analyze = st.button("Analyze Design")

# ---------------- PROMPT ----------------
def build_prompt(domain, description):
    return f"""
You are a professional engineering expert.

Domain: {domain}

Design description:
{description}

Provide a structured engineering analysis including:
- Technical overview
- Key components
- Strengths and weaknesses
- Design improvements
- Real-world applications

Please format your response with clear headings and bullet points where appropriate.
"""

# ---------------- LLM CALL ----------------
def call_llm(prompt):
    try:
        # Use the chat.completions endpoint with a supported model
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.1-8B-Instruct",  # Supported model
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=400,
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error calling the model: {str(e)}")
        st.info("This might be due to: 1) Missing 'Inference Providers' permission on your token, 2) Model not available, or 3) Rate limiting.")
        return None

# ---------------- EXECUTION ----------------
if analyze:
    if not description:
        st.warning("Please describe the design.")
    else:
        with st.spinner("🤖 AI is analyzing your design..."):
            prompt = build_prompt(domain, description)
            result = call_llm(prompt)

        if result:
            st.success("✅ Analysis Complete")
            st.markdown("---")
            st.subheader("📊 Engineering Analysis Results")
            st.markdown(result)
            
            # Add a download button for the analysis
            st.download_button(
                label="📥 Download Analysis",
                data=result,
                file_name=f"engineering_analysis_{domain.split('/')[0].lower().replace(' ', '_')}.txt",
                mime="text/plain"
            )
