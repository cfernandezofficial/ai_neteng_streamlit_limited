
import streamlit as st
from prompts import analyze_cli_output, generate_config_from_intent
import os

# --- Session state toggle for sidebar ---
if "show_sidebar" not in st.session_state:
    st.session_state.show_sidebar = False

# --- Top bar with hamburger + logo ---
st.markdown("""
<style>
    .topbar-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 20px 0 10px;
    }
    .hamburger {
        font-size: 24px;
        cursor: pointer;
        margin-top: 10px;
    }
</style>
<div class="topbar-container">
    <div class="hamburger" onclick="window.location.reload()">☰</div>
    <div>
        <img src='https://raw.githubusercontent.com/cfernandezofficial/ai_neteng_streamlit_limited/main/logo.png' alt='Nexthop AI Logo' width='150'>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Usage Notice Banner ---
st.markdown("""
<div style="
    background-color: #e8f0fe;
    padding: 12px 20px;
    border-left: 5px solid #1a73e8;
    border-radius: 8px;
    font-size: 15px;
    color: #202124;
    margin-top: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
    <strong>Usage Notice:</strong> Free tier allows up to <strong>5 prompts per session</strong>. <em>(0/5 used)</em>
</div>
""", unsafe_allow_html=True)

# --- Mode Selection with cleaner layout ---
st.markdown("""
<div style="
    margin-top: 25px;
    padding: 15px 25px;
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
""", unsafe_allow_html=True)

mode = st.radio("**Select mode:**", ["🔍 Analyze CLI/Config", "⚙️ Generate Config from Intent"])

st.markdown("</div>", unsafe_allow_html=True)


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
