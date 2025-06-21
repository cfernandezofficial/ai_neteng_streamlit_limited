import streamlit as st
from prompts import analyze_cli_output, generate_config_from_intent
import os

# --- Page config ---
st.set_page_config(page_title="Nexthop AI", layout="wide")

# --- State for chat sidebar toggle ---
if "show_sidebar" not in st.session_state:
    st.session_state.show_sidebar = False

# --- Top navbar with logo and hamburger menu ---
st.markdown("""
    <style>
        header, footer {visibility: hidden;}

        .top-nav {
            position: fixed;
            top: 0; left: 0;
            width: 100%;
            background-color: #ffffff;
            border-bottom: 1px solid #e1e1e1;
            padding: 12px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            z-index: 1000;
        }

        .top-nav .logo {
            display: flex;
            align-items: center;
        }

        .top-nav img {
            height: 38px;
            margin-left: 10px;
        }

        .hamburger {
            font-size: 24px;
            cursor: pointer;
            background: none;
            border: none;
            color: #333;
        }

        .block-container {
            padding-top: 80px;
        }

        .sidebar-panel {
            position: fixed;
            top: 60px;
            left: 0;
            width: 250px;
            height: 100%;
            background-color: #f9f9f9;
            border-right: 1px solid #ddd;
            padding: 20px;
            box-shadow: 2px 0 6px rgba(0,0,0,0.05);
            z-index: 999;
        }

        .sidebar-panel h4 {
            margin-top: 0;
        }

        .usage-banner {
            background-color: #e8f0fe;
            padding: 12px 20px;
            border-left: 5px solid #1a73e8;
            border-radius: 8px;
            font-size: 15px;
            color: #202124;
            margin-top: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
    </style>

    <div class="top-nav">
        <form method="post">
            <button name="toggle_sidebar" class="hamburger">☰</button>
        </form>
        <div class="logo">
            <img src='https://raw.githubusercontent.com/cfernandezofficial/ai_neteng_streamlit_limited/main/logo.png' alt='Nexthop AI Logo'>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- Sidebar toggle logic ---
if st.session_state.get("toggle_sidebar"):
    st.session_state.show_sidebar = not st.session_state.show_sidebar

if st.session_state.show_sidebar:
    st.markdown("""
        <div class="sidebar-panel">
            <h4>🗂️ Chat History</h4>
            <ul style="padding-left: 20px;">
                <li>BGP Config Analysis</li>
                <li>VRF + OMP Intent</li>
                <li>IP SLA with Tracking</li>
                <li>Site-to-Site VPN</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# --- Usage Banner ---
st.markdown('<div class="usage-banner"><strong>Usage Notice:</strong> Free tier allows up to <strong>5 prompts per session</strong>. <em>(0/5 used)</em></div>', unsafe_allow_html=True)

# --- Mode selection ---
st.markdown("### ⚙️ Select Mode")
mode = st.radio("", ["🔍 Analyze CLI/Config", "⚙️ Generate Config from Intent"])

st.markdown("---")

# --- API credentials check ---
api_key = os.getenv("OPENAI_API_KEY")
project_id = os.getenv("OPENAI_PROJECT_ID")

if not api_key or not project_id:
    st.warning("Missing OpenAI credentials. Set OPENAI_API_KEY and OPENAI_PROJECT_ID in your environment.")
    st.stop()

# --- Usage counter ---
if "usage_count" not in st.session_state:
    st.session_state.usage_count = 0

MAX_USES = 5
if st.session_state.usage_count >= MAX_USES:
    st.warning("🚫 You've reached the usage limit for this session. Please refresh the page or come back later.")
    st.stop()

# --- CLI Analysis Mode ---
if mode == "🔍 Analyze CLI/Config":
    st.markdown("## Paste CLI Output or Upload Config File")
    cli_text = st.text_area("Paste output here (e.g., show run, show ip bgp):", height=250)
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

# --- Intent-to-Config Mode ---
elif mode == "⚙️ Generate Config from Intent":
    st.markdown("## Describe Desired Configuration")
    intent = st.text_area("Example: 'Configure dual-WAN with BGP failover and VRFs'", height=200)

    if st.button("⚙️ Generate Config"):
        if not intent.strip():
            st.warning("Please enter an intent or description.")
        else:
            st.session_state.usage_count += 1
            with st.spinner("Generating..."):
                result = generate_config_from_intent(intent, api_key, project_id)
                st.markdown("### 🛠️ Suggested Config")
                st.code(result, language="bash")
