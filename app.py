import streamlit as st
from ai_utils import ImageAnalyzer
import os

# Page config
st.set_page_config(
    page_title="Image Analysis App",
    page_icon="🖼️",
    layout="wide"
)

# Title
st.title("🖼️ Game Analyzer Demo")
st.write("Upload an image and get AI-powered analysis")

# Initialize session state for analyzer
if 'analyzer' not in st.session_state:
    # Get API key from environment variable or Streamlit secrets
    api_key = os.getenv('GROQ_API_KEY') or st.secrets.get('groq_api_key')
    if not api_key:
        st.error("Please set the GROQ_API_KEY environment variable or add it to your Streamlit secrets.")
        st.stop()
    st.session_state.analyzer = ImageAnalyzer(api_key)

# File uploader
uploaded_file = st.file_uploader("Choose an image file", type=['png', 'jpg', 'jpeg'])

# Prompt input
prompt = st.text_input(
    "Enter your prompt",
    value="Describe what is happening in this image",
    help="What would you like to know about the image?"
)

# Analysis section
if uploaded_file and prompt:
    try:
        # Display the uploaded image
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Uploaded Image")
            st.image(uploaded_file, use_column_width=True)
        
        # Analyze the image
        with col2:
            st.subheader("Analysis")
            with st.spinner("Analyzing image..."):
                # Reset file pointer
                uploaded_file.seek(0)
                # Get analysis
                analysis = st.session_state.analyzer.analyze_image(uploaded_file, prompt)
                st.write(analysis)
                
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
else:
    st.info("Please upload an image and enter a prompt to get started.")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit and Groq's LLaMA 3.2 Vision Model")