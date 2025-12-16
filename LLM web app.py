import streamlit as st
import requests
import json
from PIL import Image
import io
import base64

# Set page configuration
st.set_page_config(
    page_title="Engineering Analysis AI",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
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
    .upload-area {
        border: 3px dashed #667eea;
        border-radius: 10px;
        padding: 3rem;
        text-align: center;
        margin: 2rem 0;
        background: #f8f9ff;
        transition: all 0.3s ease;
    }
    .upload-area:hover {
        border-color: #764ba2;
        background: #f0f2ff;
    }
    .analysis-result {
        background: #f8f9ff;
        border-left: 5px solid #667eea;
        padding: 1.5rem;
        border-radius: 8px;
        margin-top: 2rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    }
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 1rem;
        border-radius: 8px;
        font-size: 1.1rem;
        font-weight: 600;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Title and header
st.markdown('<div class="logo">🔧</div>', unsafe_allow_html=True)
st.markdown('<div class="main-header"><h1>Engineering Analysis AI</h1><p>Upload your design and get expert technical analysis</p></div>', unsafe_allow_html=True)

# Initialize session state
if 'image_uploaded' not in st.session_state:
    st.session_state.image_uploaded = False
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'image_data' not in st.session_state:
    st.session_state.image_data = None

# Sidebar for Ollama configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    ollama_url = st.text_input(
        "Ollama Server URL",
        value="http://localhost:11434",
        help="URL of your Ollama server. For local setup, use http://localhost:11434"
    )
    model_name = st.text_input(
        "Model Name",
        value="tinyllama:latest",
        help="Name of the Ollama model to use"
    )
    
    st.markdown("---")
    st.markdown("### 📖 Instructions")
    st.markdown("""
    1. Make sure Ollama is running locally
    2. Pull the model: `ollama pull tinyllama:latest`
    3. Run Ollama server
    4. Upload your design image
    5. Select domain and describe your design
    6. Click 'Analyze Design'
    """)

# Main content
col1, col2 = st.columns(2)

with col1:
    st.subheader("📁 Upload Your Design")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['jpg', 'jpeg', 'png', 'gif'],
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        # Display image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Design", use_column_width=True)
        
        # Store image data
        st.session_state.image_uploaded = True
        st.session_state.image_data = uploaded_file.getvalue()
        
        st.markdown('<div class="success-message">✅ Image uploaded successfully!</div>', unsafe_allow_html=True)

with col2:
    st.subheader("🎯 Analysis Settings")
    
    # Domain selection
    domain = st.selectbox(
        "🏷️ What type of design is this?",
        options=["", "robotics", "product", "cad", "mechanism", "electronics", "other"],
        format_func=lambda x: {
            "": "-- Select the domain --",
            "robotics": "🤖 Robotics / Mechanical Systems",
            "product": "📱 Product Design",
            "cad": "💻 CAD Model / 3D Design",
            "mechanism": "⚙️ Mechanical Mechanism",
            "electronics": "🔌 Electronics / PCB Design",
            "other": "🔍 Other Engineering Design"
        }[x]
    )
    
    # Description input
    description = st.text_area(
        "📝 Describe what you see in the image:",
        height=150,
        placeholder="Example: 'This is a 4-degree-of-freedom robotic arm with servo motors, aluminum frame, and a gripper mechanism. The joints appear to use rotary actuators...'",
        help="Be specific about: Components, materials, mechanisms, intended function"
    )

# Analysis button
if st.button("🚀 Analyze Design", type="primary"):
    if not st.session_state.image_uploaded:
        st.error("⚠️ Please upload an image first!")
    elif not domain:
        st.error("⚠️ Please select a domain!")
    elif not description.strip():
        st.error("⚠️ Please describe your design!")
    else:
        with st.spinner("🤖 AI is analyzing your design... This may take a few seconds"):
            try:
                # Domain-specific prompts
                domain_prompts = {
                    "robotics": f"""You are a robotics engineering expert. Analyze this robotic system: "{description}"

Provide a comprehensive technical analysis:

🔧 TECHNICAL SPECIFICATIONS:
- Mechanism type and degrees of freedom
- Key components and their functions
- Actuation methods and power requirements
- Control system architecture
- Performance capabilities

⚙️ DESIGN CONSIDERATIONS:
- Potential applications and use cases
- Strengths and limitations
- Suggested improvements
- Safety considerations
- Integration possibilities""",

                    "product": f"""You are a product design expert. Analyze this product design: "{description}"

Provide a comprehensive design analysis:

🎯 PRODUCT ANALYSIS:
- Intended function and target users
- Key features and differentiators
- Ergonomics and user experience
- Aesthetic considerations
- Market positioning

🏭 MANUFACTURING & COST:
- Suitable materials and processes
- Manufacturing complexity
- Cost optimization opportunities
- Assembly considerations
- Sustainability aspects""",

                    "cad": f"""You are a CAD and mechanical design expert. Analyze this 3D model: "{description}"

Provide a comprehensive CAD analysis:

📐 DESIGN EVALUATION:
- Geometric complexity and features
- Functional requirements fulfillment
- Design for manufacturability
- Tolerance and fit considerations
- Potential stress points

🛠️ ENGINEERING RECOMMENDATIONS:
- Suggested design improvements
- Material selection guidance
- Manufacturing process recommendations
- Prototyping considerations
- Testing and validation approach""",

                    "mechanism": f"""You are a mechanical engineering expert. Analyze this mechanism: "{description}"

Provide a comprehensive mechanical analysis:

⚙️ MECHANICAL ANALYSIS:
- Type of mechanism and principle of operation
- Kinematic chain and mobility
- Force transmission and efficiency
- Component interactions
- Motion characteristics

🔧 PERFORMANCE & OPTIMIZATION:
- Potential failure points
- Wear and maintenance considerations
- Efficiency improvements
- Alternative mechanism options
- Load capacity and limitations""",

                    "electronics": f"""You are an electronics engineering expert. Analyze this electronic design: "{description}"

Provide a comprehensive electronics analysis:

🔌 ELECTRONIC ANALYSIS:
- Circuit functionality and components
- Power requirements and management
- Signal flow and processing
- Component selection rationale
- Integration capabilities

⚡ DESIGN CONSIDERATIONS:
- PCB layout considerations
- Thermal management
- EMI/EMC considerations
- Testing and debugging approach
- Reliability factors""",

                    "other": f"""You are an engineering expert. Analyze this design: "{description}"

Provide a comprehensive engineering analysis:

🔍 TECHNICAL ASSESSMENT:
- Design purpose and functionality
- Key engineering principles applied
- Component relationships and interactions
- Performance characteristics
- Innovation aspects

💡 RECOMMENDATIONS:
- Potential improvements
- Alternative approaches
- Implementation considerations
- Risk factors and mitigation
- Future development opportunities"""
                }
                
                # Prepare request
                request_data = {
                    "model": model_name,
                    "prompt": domain_prompts[domain],
                    "stream": False
                }
                
                # Send request to Ollama
                response = requests.post(
                    f"{ollama_url}/api/generate",
                    json=request_data,
                    timeout=60
                )
                
                if response.status_code == 200:
                    analysis_data = response.json()
                    st.session_state.analysis_result = analysis_data.get("response", "")
                else:
                    st.error(f"❌ Ollama API Error: {response.status_code}")
                    st.session_state.analysis_result = None
                    
            except requests.exceptions.ConnectionError:
                st.error("🚫 Cannot connect to Ollama server. Make sure Ollama is running!")
            except requests.exceptions.Timeout:
                st.error("⏰ Request timed out. The server might be busy or slow.")
            except Exception as e:
                st.error(f"⚠️ An error occurred: {str(e)}")

# Display analysis results
if st.session_state.analysis_result:
    st.markdown("---")
    st.subheader("📊 Analysis Results")
    
    with st.container():
        st.markdown(f"""
        <div class="analysis-result">
            <h3>🔍 Engineering Analysis Results</h3>
            <div style="white-space: pre-wrap; line-height: 1.6; margin-top: 1rem;">
                {st.session_state.analysis_result}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Download button for results
    st.download_button(
        label="📥 Download Analysis",
        data=st.session_state.analysis_result,
        file_name="engineering_analysis.txt",
        mime="text/plain"
    )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; padding: 2rem;">
    <p><strong>Engineering Analysis AI</strong> | Powered by Ollama & Streamlit</p>
    <p>For best results, provide detailed descriptions of your designs.</p>
</div>
""", unsafe_allow_html=True)