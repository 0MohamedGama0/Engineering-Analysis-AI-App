import streamlit as st
import base64
from PIL import Image
import io
import openai  # Make sure to add "openai>=1.0.0" to your requirements.txt

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
# Reliable models that work well with Hugging Face Inference Providers (free tier compatible)
VISION_MODEL = "Qwen/Qwen2.5-VL-7B-Instruct"        # Excellent vision-language model
TEXT_MODEL   = "meta-llama/Meta-Llama-3.1-8B-Instruct"  # Strong text analysis model

HF_API_KEY = st.secrets.get("HF_API_KEY")
if not HF_API_KEY:
    st.error("HF_API_KEY is missing. Please add it in Streamlit Secrets.")
    st.stop()

# Use OpenAI-compatible client pointed at Hugging Face router
client = openai.OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_API_KEY
)

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
    """Call the vision-language model to describe the engineering content in the image"""
    img_b64 = image_to_base64(image)
    try:
        completion = client.chat.completions.create(
            model=VISION_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{img_b64}"
                            }
                        },
                        {
                            "type": "text",
                            "text": "Carefully examine the image and provide a detailed technical description of the engineering object, system, or component shown. Include visible parts, materials (if apparent), connections, mechanisms, and any labels or markings."
                        }
                    ]
                }
            ],
            max_tokens=600,
            temperature=0.4
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"VISION_ERROR: {str(e)}"

def text_only_analysis(text_input: str, domain: str) -> str:
    """Use a text-only LLM to perform structured engineering analysis"""
    prompt = f"""
You are an expert engineering analyst specializing in {domain}.

IMAGE/OBJECT DESCRIPTION:
{text_input}

TASK:
Provide a clear, structured engineering analysis with the following sections:

1. **Identification**: What is the object or system shown?
2. **Key Components**: List and briefly describe the main parts visible.
3. **Functionality**: Explain how it works or what it is designed to do.
4. **Design Strengths**: Highlight good engineering choices (stability, efficiency, modularity, etc.).
5. **Potential Limitations or Risks**: Note any weaknesses, failure points, or safety concerns.
6. **Suggested Improvements**: Offer practical recommendations for better performance, manufacturability, or reliability.

Use bullet points or numbered lists for clarity. Be objective and technical.
"""
    try:
        completion = client.chat.completions.create(
            model=TEXT_MODEL,
            messages=[
                {"role": "system", "content": "You are a precise and knowledgeable engineering analyst."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.4
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"TEXT_ERROR: {str(e)}"

# --------------------------------------------------
# UI Layout
# --------------------------------------------------
st.title("🔧 Engineering Analysis AI")
st.caption("Vision-Language Engineering Analysis with Reliable Fallback • Powered by Hugging Face Inference")

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
        "Engineering Domain",
        [
            "Robotics / Mechanical Systems",
            "Product Design",
            "CAD Model / 3D Printed",
            "Electronics / PCB Design"
        ]
    )
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        if st.button("🔍 Analyze Image (Vision Model)", use_container_width=True):
            with st.spinner("Running vision-language analysis..."):
                result = vision_language_analysis(image)
            
            if result.startswith("VISION_ERROR"):
                st.session_state.vl_failed = True
                st.error("Vision model failed: " + result)
                st.warning("Switching to fallback mode. Please provide a manual description below.")
            else:
                st.session_state.vision_result = result
                st.session_state.vl_failed = False
                st.success("Image successfully analyzed!")
    
    # Fallback manual input
    if st.session_state.vl_failed or (uploaded_file and not st.session_state.vision_result):
        manual_input = st.text_area(
            "📝 Manual Description (Fallback Mode)",
            placeholder="Example: A 4-DOF robotic arm with servo motors, aluminum links, and an end-effector gripper mounted on a fixed base.",
            height=150
        )
        if st.button("📊 Analyze via Text Model", use_container_width=True):
            if manual_input.strip():
                with st.spinner("Running engineering analysis..."):
                    result = text_only_analysis(manual_input.strip(), domain)
                    if result.startswith("TEXT_ERROR"):
                        st.error(result)
                    else:
                        st.session_state.final_analysis = result
            else:
                st.warning("Please enter a description.")

# --------------------------------------------------
# Right Column: Results
# --------------------------------------------------
with right:
    st.subheader("Results")
    
    if st.session_state.vision_result:
        st.markdown("### 🧠 AI Image Understanding")
        st.write(st.session_state.vision_result)
        
        if st.button("📊 Generate Full Engineering Analysis", use_container_width=True):
            with st.spinner("Generating detailed engineering analysis..."):
                result = text_only_analysis(st.session_state.vision_result, domain)
                if result.startswith("TEXT_ERROR"):
                    st.error(result)
                else:
                    st.session_state.final_analysis = result
    
    if st.session_state.final_analysis:
        st.markdown("### 📊 Engineering Analysis")
        st.markdown(st.session_state.final_analysis)

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("---")
st.caption("Note: This app uses Hugging Face Inference Providers (free tier). Heavy usage may hit rate limits. For production use, consider HF Pro or dedicated endpoints.")
