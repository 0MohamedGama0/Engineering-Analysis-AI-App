import streamlit as st
from PIL import Image
import io
import base64

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Engineering Analysis AI",
    page_icon="🔧",
    layout="wide"
)

# --------------------------------------------------
# Session State
# --------------------------------------------------
if "vision_result" not in st.session_state:
    st.session_state.vision_result = ""

if "final_analysis" not in st.session_state:
    st.session_state.final_analysis = ""

if "error_message" not in st.session_state:
    st.session_state.error_message = ""

# --------------------------------------------------
# Helper Functions
# --------------------------------------------------
def image_to_base64(image: Image.Image) -> str:
    """Convert PIL Image to base64 string"""
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def analyze_image_with_streamlit(image: Image.Image, domain: str) -> tuple:
    """
    Analyze image using Streamlit's built-in chat_model
    Returns: (vision_description, full_analysis, error_message)
    """
    try:
        # Convert image to base64
        img_b64 = image_to_base64(image)
        
        # Step 1: Get image description
        vision_prompt = """Describe the engineering object or system in this image in detail. 
Focus on:
- What type of engineering system/object it is
- Visible components and parts
- Materials and construction
- Any notable features or characteristics"""

        vision_response = st.chat_model(
            "claude-3-5-sonnet-20241022",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": img_b64}},
                    {"type": "text", "text": vision_prompt}
                ]
            }]
        )
        
        vision_description = vision_response.content[0].text
        
        # Step 2: Generate engineering analysis based on vision description
        analysis_prompt = f"""You are an expert engineering analyst specializing in {domain}.

Based on the following description of an engineering system/object:

{vision_description}

Provide a comprehensive engineering analysis with the following structure:

## System Identification
[Identify what the system/object is]

## Key Components
[List and describe the main components]

## Functionality & Operation
[Explain how it works]

## Design Strengths
[Highlight positive design aspects]

## Potential Limitations or Risks
[Identify any concerns or weaknesses]

## Suggested Improvements
[Recommend enhancements or optimizations]

Be specific, technical, and professional in your analysis."""

        analysis_response = st.chat_model(
            "claude-3-5-sonnet-20241022",
            messages=[{
                "role": "user",
                "content": analysis_prompt
            }]
        )
        
        full_analysis = analysis_response.content[0].text
        
        return vision_description, full_analysis, ""
        
    except Exception as e:
        error_msg = f"Error with Streamlit chat_model: {str(e)}"
        return "", "", error_msg


def analyze_text_only(description: str, domain: str) -> str:
    """Fallback: Analyze based on text description only"""
    try:
        prompt = f"""You are an expert engineering analyst specializing in {domain}.

Based on the following description:

{description}

Provide a comprehensive engineering analysis with the following structure:

## System Identification
[Identify what the system/object is]

## Key Components
[List and describe the main components]

## Functionality & Operation
[Explain how it works]

## Design Strengths
[Highlight positive design aspects]

## Potential Limitations or Risks
[Identify any concerns or weaknesses]

## Suggested Improvements
[Recommend enhancements or optimizations]

Be specific, technical, and professional in your analysis."""

        response = st.chat_model(
            "claude-3-5-sonnet-20241022",
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        return response.content[0].text
        
    except Exception as e:
        return f"Error generating analysis: {str(e)}"


# --------------------------------------------------
# UI Layout
# --------------------------------------------------
st.title("🔧 Engineering Analysis AI")
st.caption("Powered by Streamlit's Built-in AI Models")

# Add info about the model being used
with st.expander("ℹ️ About this tool"):
    st.markdown("""
    This tool uses **Streamlit's built-in `st.chat_model`** with Claude 3.5 Sonnet to:
    1. Analyze engineering images using vision capabilities
    2. Generate detailed technical analysis
    3. Provide expert insights and recommendations
    
    No external API keys required!
    """)

left, right = st.columns(2)

# --------------------------------------------------
# Left Column: Inputs
# --------------------------------------------------
with left:
    st.subheader("📥 Input")

    uploaded_file = st.file_uploader(
        "Upload an engineering-related image (JPG / PNG)",
        type=["jpg", "jpeg", "png"],
        help="Upload images of robots, mechanical systems, CAD models, PCBs, etc."
    )

    domain = st.selectbox(
        "Select the engineering domain",
        [
            "Robotics / Mechanical Systems",
            "Product Design",
            "CAD Model / 3D Printed Objects",
            "Electronics / PCB Design",
            "Civil Engineering / Structures",
            "Aerospace Engineering",
            "Automotive Engineering",
            "Manufacturing / Industrial"
        ]
    )

  

