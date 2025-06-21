
import streamlit as st
from prompts import analyze_cli_output, generate_config_from_intent
import os

st.set_page_config(page_title="Nexthop AI", layout="wide")

# --- Custom CSS Styling ---
st.markdown("""
    <style>
        .main {background-color: #f8f9fa;}
        h1 {color: #333333;}
        .stButton button {background-color: #0052cc; color: white; font-weight: bold;}
        .stRadio > div {padding: 5px 0;}
        .custom-header {text-align: center; margin-bottom: 20px;}
        hr {border: none; height: 1px; background-color: #ddd; margin: 30px 0;}
        .upload-box {border: 1px solid #ccc; padding: 20px; background-color: #ffffff; border-radius: 8px;}
    </style>
""", unsafe_allow_html=True)

# --- Branded Header Section ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
<div style='text-align: center; margin-top: -150px; margin-bottom: -10px;'>
    <img src='https://raw.githubusercontent.com/cfernandezofficial/ai_neteng_streamlit_limited/main/logo.png' alt='Nexthop AI Logo' width='300'>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown("""
<div style="
    background-color: #e8f0fe;
    padding: 12px 20px;
    border-left: 6px solid #1a73e8;
    border-radius: 6px;
    font-size: 15px;
    color: #202124;
    margin-bottom: 20px;">
    <strong>Usage Notice:</strong> Free tier allows up to <strong>5 prompts per session</strong>. <em>(0/5 used)</em>
</div>
""", unsafe_allow_html=True)

# --- Mode Selection ---
mode = st.radio("Select mode:", ["🔍 Analyze CLI/Config", "⚙️ Generate Config from Intent"])

st.markdown("<hr>", unsafe_allow_html=True)

# API credentials from Streamlit Secrets
api_key = os.getenv("OPENAI_API_KEY")
project_id = os.getenv("OPENAI_PROJECT_ID")

if not api_key or not project_id:
    st.warning("Missing OpenAI credentials. Set OPENAI_API_KEY and OPENAI_PROJECT_ID in Streamlit secrets.")
    st.stop()

# Initialize usage count
if "usage_count" not in st.session_state:
    st.session_state.usage_count = 0

MAX_USES = 5

if st.session_state.usage_count >= MAX_USES:
    st.warning("🚫 You've reached the usage limit for this session. Please refresh the page or come back later.")
    st.stop()

if mode == "🔍 Analyze CLI/Config":
    st.subheader("Paste CLI Output or Upload Config File")
    cli_text = st.text_area("Paste output here (e.g., show run, show ip bgp):", height=250)
    uploaded_file = st.file_uploader("Or upload a .txt config file", type=["txt"])

    if uploaded_file is not None:
        cli_text = uploaded_file.read().decode("utf-8")

    if st.button("Analyze"):
        if not cli_text.strip():
            st.warning("Please paste output or upload a config file.")
        else:
            st.session_state.usage_count += 1
            with st.spinner("Analyzing..."):
                result = analyze_cli_output(cli_text, api_key, project_id)
                st.markdown("### 🔍 AI Analysis")
                st.write(result)

elif mode == "⚙️ Generate Config from Intent":
    st.subheader("Describe the desired configuration behavior")
    intent = st.text_area("Example: 'Configure dual-WAN with BGP failover and VRFs'", height=200)

    if st.button("Generate Config"):
        if not intent.strip():
            st.warning("Please enter an intent or description.")
        else:
            st.session_state.usage_count += 1
            with st.spinner("Generating..."):
                result = generate_config_from_intent(intent, api_key, project_id)
                st.markdown("### 🛠️ Suggested Config")
                st.code(result, language="bash")
