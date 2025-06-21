# Streamlined Nexthop AI Frontend (Fixed Mode Crash, Larger Logo, Tight Layout)

import streamlit as st
from prompts import analyze_cli_output, generate_config_from_intent
import os
import base64

st.set_page_config(page_title="Nexthop AI", layout="wide")

# --- Session Defaults ---
if "usage_count" not in st.session_state:
    st.session_state.usage_count = 0
if "mode" not in st.session_state:
    st.session_state.mode = "🔍 Analyze CLI/Config"

# --- Styling ---
st.markdown("""
    <style>
        html, body {
            background-color: #f4f4f4;
            font-family: 'Segoe UI', sans-serif;
            color: #111;
            margin: 0;
            padding: 0;
        }

        header, footer { visibility: hidden; }

        .main-area {
            padding: 20px 60px;
        }

        .card {
            background-color: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            max-width: 900px;
            margin: 16px auto;
        }

        .center-logo {
            display: flex;
            justify-content: center;
            margin: 10px auto 0;
        }

        .mode-selector {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin: 10px auto 0;
        }

        .mode-button {
            background-color: white;
            border: 2px solid #ddd;
            border-radius: 10px;
            padding: 12px 24px;
            font-size: 15px;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        }

        .mode-button:hover, .mode-button.active {
            border-color: #3b82f6;
            background-color: #e0edff;
            color: #1d4ed8;
        }

        .stTextArea textarea {
            padding: 12px;
            font-size: 14px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Logo Centered ---
st.markdown("""
    <div class='center-logo'>
        <img src="https://raw.githubusercontent.com/cfernandezofficial/ai_neteng_streamlit_limited/main/logo.png" width="260">
    </div>
""", unsafe_allow_html=True)

st.markdown("<div class='main-area'>", unsafe_allow_html=True)

# --- Usage Notice ---
st.markdown(f"""
<div class='card' style='margin-top: 10px;'>
    <strong>Usage Notice:</strong> Free tier allows up to <strong>5 prompts per session</strong>. <em>({st.session_state.usage_count}/5 used)</em>
</div>
""", unsafe_allow_html=True)

# --- Mode Selector ---
st.markdown("<div class='mode-selector'>", unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🔍 Analyze CLI/Config"):
        st.session_state.mode = "🔍 Analyze CLI/Config"
with col2:
    if st.button("⚙️ Generate Config from Intent"):
        st.session_state.mode = "⚙️ Generate Config from Intent"
st.markdown("</div>", unsafe_allow_html=True)

# --- API credentials check ---
api_key = os.getenv("OPENAI_API_KEY")
project_id = os.getenv("OPENAI_PROJECT_ID")
if not api_key or not project_id:
    st.warning("Missing OpenAI credentials. Set OPENAI_API_KEY and OPENAI_PROJECT_ID in your environment.")
    st.stop()

MAX_USES = 5
if st.session_state.usage_count >= MAX_USES:
    st.warning("🚫 You've reached the usage limit for this session. Please refresh the page or come back later.")
    st.stop()

# --- CLI Analysis Mode ---
if st.session_state.mode == "🔍 Analyze CLI/Config":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Paste CLI Output or Upload Config File")
    cli_text = st.text_area("Paste output here (e.g., show run, show ip bgp):", height=200)
    uploaded_file = st.file_uploader("Or upload a .txt config file", type=["txt"])
    if uploaded_file is not None:
        cli_text = uploaded_file.read().decode("utf-8")

    if st.button("🔎 Analyze"):
        if not cli_text.strip():
            st.warning("Please paste output or upload a config file.")
        else:
            st.session_state.usage_count += 1
            with st.spinner("Analyzing..."):
                result = analyze_cli_output(cli_text, api_key, project_id)
                st.markdown("### 🔍 AI Analysis")
                st.write(result)
                b64 = base64.b64encode(result.encode()).decode()
                href = f'<a href="data:file/txt;base64,{b64}" download="analysis.txt">💾 Download Analysis as .txt</a>'
                st.markdown(href, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- Intent Mode ---
elif st.session_state.mode == "⚙️ Generate Config from Intent":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Describe Desired Configuration")
    intent = st.text_area("Example: 'Configure dual-WAN with BGP failover and VRFs'", height=160)

    if st.button("⚙️ Generate Config"):
        if not intent.strip():
            st.warning("Please enter an intent or description.")
        else:
            st.session_state.usage_count += 1
            with st.spinner("Generating..."):
                result = generate_config_from_intent(intent, api_key, project_id)
                st.markdown("### 🛠️ Suggested Config")
                st.code(result, language="bash")
                b64 = base64.b64encode(result.encode()).decode()
                href = f'<a href="data:file/txt;base64,{b64}" download="generated_config.txt">💾 Download Config as .txt</a>'
                st.markdown(href, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)