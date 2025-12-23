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

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Image", use_container_width=True)

        if st.button("🚀 Analyze Image", type="primary", use_container_width=True):
            st.session_state.vision_result = ""
            st.session_state.final_analysis = ""
            st.session_state.error_message = ""
            
            with st.spinner("Analyzing image with AI vision model..."):
                vision_desc, analysis, error = analyze_image_with_streamlit(image, domain)
                
                if error:
                    st.session_state.error_message = error
                    st.error(error)
                else:
                    st.session_state.vision_result = vision_desc
                    st.session_state.final_analysis = analysis
                    st.success("✅ Analysis complete!")

    st.divider()
    
    # Manual input fallback
    st.subheader("📝 Manual Input (Optional)")
    st.caption("Use this if you don't have an image or want to analyze a text description")
    
    manual_description = st.text_area(
        "Describe the engineering system",
        placeholder="Example: A 6-DOF robotic arm with servo motors, aluminum frame, and parallel jaw gripper. The arm has a reach of approximately 50cm and appears to use a microcontroller-based control system.",
        height=100
    )
    
    if st.button("🔍 Analyze Description", use_container_width=True):
        if manual_description.strip():
            st.session_state.vision_result = manual_description
            st.session_state.error_message = ""
            
            with st.spinner("Generating engineering analysis..."):
                analysis = analyze_text_only(manual_description, domain)
                st.session_state.final_analysis = analysis
                st.success("✅ Analysis complete!")
        else:
            st.warning("Please enter a description first.")

# --------------------------------------------------
# Right Column: Results
# --------------------------------------------------
with right:
    st.subheader("📊 Results")

    if st.session_state.error_message:
        st.error(f"**Error:** {st.session_state.error_message}")
        st.info("💡 Try using the manual input option below the image upload.")

    if st.session_state.vision_result:
        with st.expander("🔍 Image/System Description", expanded=True):
            st.markdown(st.session_state.vision_result)

    if st.session_state.final_analysis:
        with st.expander("📋 Engineering Analysis", expanded=True):
            st.markdown(st.session_state.final_analysis)
        
        # Download option
        st.download_button(
            label="📥 Download Analysis",
            data=f"# Engineering Analysis\n\n## Domain: {domain}\n\n## Description\n{st.session_state.vision_result}\n\n## Analysis\n{st.session_state.final_analysis}",
            file_name="engineering_analysis.md",
            mime="text/markdown"
        )

    if not st.session_state.vision_result and not st.session_state.final_analysis:
        st.info("👆 Upload an image or enter a description to get started")

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.divider()
st.caption("Built with Streamlit • Powered by Claude 3.5 Sonnet")
