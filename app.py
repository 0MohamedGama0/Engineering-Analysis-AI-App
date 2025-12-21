import streamlit as st
from PIL import Image
from huggingface_hub import InferenceClient
import os

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Engineering Analysis AI",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
    }
    .logo {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    .analysis-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #3498db;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
    }
    .demo-notice {
        background: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
        border-left: 4px solid #ffc107;
    }
</style>
""", unsafe_allow_html=True)

# ==================== INITIALIZATION ====================
# Get API key from Streamlit secrets
HF_API_KEY = st.secrets.get("HF_API_KEY", os.environ.get("HF_API_KEY", None))

# Initialize Hugging Face clients if API key is available
if HF_API_KEY:
    vision_client = InferenceClient(model="Salesforce/blip-image-captioning-base", token=HF_API_KEY)
    text_client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.2", token=HF_API_KEY)
else:
    vision_client = None
    text_client = None

# ==================== FUNCTIONS ====================
def vision_caption(image: Image.Image) -> str:
    """Generate caption using Hugging Face vision model"""
    if not vision_client:
        return "[DEMO] This would describe the uploaded image. Real analysis requires Hugging Face API key."
    
    try:
        result = vision_client.image_to_text(image=image)
        return result
    except Exception as e:
        return f"Vision model error: {str(e)}"

def engineering_analysis(caption: str, user_description: str, domain: str) -> str:
    """Generate engineering analysis using Hugging Face LLM"""
    if not text_client:
        return f"""[DEMO] Engineering Analysis for {domain}
        
Based on your description: "{user_description[:100]}..."

✅ TECHNICAL ASSESSMENT:
- Design appears functional and well-structured
- Appropriate materials and mechanisms for intended use
- Good consideration of user requirements

⚠️ RECOMMENDATIONS:
1. Conduct detailed stress analysis
2. Prototype and test with real users
3. Consider manufacturing constraints
4. Evaluate cost optimization opportunities

📈 NEXT STEPS:
- Create detailed CAD models
- Build functional prototype
- Test in real-world conditions
- Iterate based on feedback"""
    
    prompt = f"""
You are an expert engineering AI analyzing design images.

DOMAIN: {domain}

IMAGE UNDERSTANDING:
{caption}

USER DESCRIPTION:
{user_description if user_description else "No additional description provided."}

TASK: Provide structured engineering analysis including:
1. System/Component Identification
2. Key Technical Specifications
3. Design Strengths & Weaknesses
4. Manufacturing Considerations
5. Improvement Suggestions
6. Safety & Reliability Factors

Format response with clear sections and bullet points.
"""
    
    try:
        result = text_client.text_generation(
            prompt=prompt,
            max_new_tokens=500,
            temperature=0.4
        )
        return result
    except Exception as e:
        return f"Text model error: {str(e)}"

# ==================== SIDEBAR ====================
with st.sidebar:
    st.title("⚙️ Configuration")
    
    st.markdown("---")
    st.subheader("🔑 API Status")
    
    if HF_API_KEY:
        st.success("✅ Hugging Face API Connected")
        st.caption("Real AI analysis enabled")
    else:
        st.warning("⚠️ DEMO MODE")
        st.caption("Add HF_API_KEY to secrets for full functionality")
    
    st.markdown("---")
    st.subheader("ℹ️ About")
    
    st.info("""
    **Engineering Analysis AI** provides:
    
    - 🤖 Technical design analysis
    - 🔍 Engineering recommendations
    - ⚙️ Manufacturing considerations
    - 🎯 Improvement suggestions
    
    *Assignment 4 - LLM Web App Deployment*
    """)
    
    st.markdown("---")
    st.caption("Built with Streamlit & Hugging Face")

# ==================== MAIN CONTENT ====================
# Title
st.markdown('<div class="logo">🔧</div>', unsafe_allow_html=True)
st.markdown('<div class="main-header"><h1>Engineering Analysis AI</h1><p>Upload your design and get expert AI-powered engineering analysis</p></div>', unsafe_allow_html=True)

# Demo notice if no API key
if not HF_API_KEY:
    st.markdown("""
    <div class="demo-notice">
    ⚠️ <strong>DEMO MODE</strong> - Showing interface and workflow. 
    For full AI functionality, add Hugging Face API key to Streamlit secrets.
    </div>
    """, unsafe_allow_html=True)

# ==================== FORM INPUTS ====================
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📁 Upload Your Design")
    
    uploaded_file = st.file_uploader(
        "Choose an engineering design image",
        type=['jpg', 'jpeg', 'png', 'gif'],
        help="CAD models, robotics, mechanisms, products, etc."
    )
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Design", use_column_width=True)
        if HF_API_KEY:
            st.success("✅ Image ready for analysis")
        else:
            st.info("📄 Image uploaded (demo mode)")

with col2:
    st.subheader("🎯 Analysis Settings")
    
    domain = st.selectbox(
        "🏷️ What type of design is this?",
        options=["Robotics / Mechanical Systems", "Product Design", "CAD Model / 3D Design", 
                 "Mechanical Mechanism", "Electronics / PCB Design", "Other Engineering Design"]
    )
    
    description = st.text_area(
        "📝 Describe what you see in the image:",
        height=150,
        placeholder="Example: 'This is a 4-degree-of-freedom robotic arm with servo motors, aluminum frame, and gripper mechanism...'",
        help="Be specific about components, materials, mechanisms, and intended function"
    )

# ==================== ANALYSIS BUTTON ====================
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyze_button = st.button(
        "🚀 Generate Engineering Analysis",
        type="primary",
        use_container_width=True,
        disabled=not uploaded_file
    )

# ==================== ANALYSIS RESULTS ====================
if analyze_button and uploaded_file:
    with st.spinner("🤖 AI is analyzing your design..."):
        # Generate analysis
        caption = vision_caption(image)
        analysis = engineering_analysis(caption, description, domain)
    
    # Display results
    st.subheader("🧠 AI Image Understanding")
    st.info(caption)
    
    st.subheader("📊 Engineering Analysis Results")
    
    with st.container():
        st.markdown("""
        <div class="analysis-card">
        """, unsafe_allow_html=True)
        
        st.markdown(analysis)
        
        st.markdown("""
        </div>
        """, unsafe_allow_html=True)
    
    # Download button
    st.download_button(
        label="📥 Download Analysis Report",
        data=analysis,
        file_name=f"engineering_analysis_{domain.replace(' ', '_')}.txt",
        mime="text/plain",
        use_container_width=True
    )

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; padding: 2rem;">
    <p><strong>Engineering Analysis AI</strong> | Assignment 4 - LLM Web App Deployment</p>
    <p><small>Course: Large Language Models | Student: [Your Name]</small></p>
</div>
""", unsafe_allow_html=True)