import streamlit as st
from prompts import analyze_cli_output, generate_config_from_intent
import os
import base64

# --- Page config ---
st.set_page_config(page_title="Nexthop AI", layout="wide")

# --- State setup ---
if "show_sidebar" not in st.session_state:
    st.session_state.show_sidebar = True
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "current_section" not in st.session_state:
    st.session_state.current_section = "chat"
if "usage_count" not in st.session_state:
    st.session_state.usage_count = 0

# --- Styling ---
base_bg = "#f4f4f4"  # Grok-like light gray background
text_color = "#111"
card_bg = "white"
border_color = "#e4e4e7"

margin_left = "260px" if st.session_state.show_sidebar else "0"

st.markdown(f"""
    <style>
        html, body {{
            background-color: {base_bg};
            color: {text_color};
            font-family: 'Segoe UI', sans-serif;
        }}

        header, footer {{visibility: hidden;}}

        .sidebar {{
            position: fixed;
            top: 0; left: 0;
            width: 240px;
            height: 100%;
            background-color: white;
            border-right: 1px solid {border_color};
            padding: 20px 16px;
            display: {'flex' if st.session_state.show_sidebar else 'none'};
            flex-direction: column;
            gap: 20px;
            z-index: 1000;
            transition: all 0.3s ease;
        }}

        .sidebar a {{
            text-decoration: none;
            color: {text_color};
            font-size: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .sidebar a:hover {{
            color: #3b82f6;
            font-weight: 500;
        }}

        .sidebar input {{
            width: 100%;
            padding: 8px 10px;
            border-radius: 6px;
            border: 1px solid #ddd;
            margin-top: 10px;
        }}

        .main-area {{
            margin-left: {margin_left};
            padding: 40px;
            transition: margin-left 0.3s ease;
        }}

        .card {{
            background-color: {card_bg};
            padding: 30px;
            border-radius: 16px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.03);
            max-width: 800px;
            margin: auto;
            color: {text_color};
        }}

        .chat-box {{
            background-color: white;
            padding: 25px;
            border-radius: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            max-width: 700px;
            margin: 60px auto 20px;
        }}

        .chat-options button {{
            margin: 6px 6px 0 0;
            padding: 10px 16px;
            border-radius: 999px;
            border: 1px solid #ddd;
            background-color: white;
            cursor: pointer;
        }}
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Navigation ---
st.markdown(f"""
    <div class="sidebar">
        <img src="https://raw.githubusercontent.com/cfernandezofficial/ai_neteng_streamlit_limited/main/logo.png" width="120" style="margin-bottom: 10px;">
        <input type="text" placeholder="Search Ctrl+K">
        <a href="#">💬 Chat</a>
        <a href="#">📁 Workspaces</a>
        <a href="#">🕘 History</a>
    </div>
""", unsafe_allow_html=True)

# --- Sidebar toggle ---
if st.button("☰ Toggle Sidebar"):
    st.session_state.show_sidebar = not st.session_state.show_sidebar

# --- Main content starts ---
st.markdown("<div class='main-area'>", unsafe_allow_html=True)

# --- Dark Mode Toggle ---
if st.toggle("🌓 Dark Mode", value=st.session_state.dark_mode):
    st.session_state.dark_mode = True
else:
    st.session_state.dark_mode = False

# --- Usage Notice ---
st.markdown(f"""
<div class='card' style='margin-bottom: 30px;'>
    <strong>Usage Notice:</strong> Free tier allows up to <strong>5 prompts per session</strong>. <em>({st.session_state.usage_count}/5 used)</em>
</div>
""", unsafe_allow_html=True)

# --- Chat Box ---
st.markdown("""
    <div class='chat-box'>
        <h4>What do you want to know?</h4>
    </div>
""", unsafe_allow_html=True)

mode = st.radio("Select Mode", ["🔍 Analyze CLI/Config", "⚙️ Generate Config from Intent"], horizontal=True)

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
if mode == "🔍 Analyze CLI/Config":
    st.markdown(f"<div class='card'>", unsafe_allow_html=True)
    st.subheader("Paste CLI Output or Upload Config File")
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

                # Export as .txt
                b64 = base64.b64encode(result.encode()).decode()
                href = f'<a href="data:file/txt;base64,{b64}" download="analysis.txt">💾 Download Analysis as .txt</a>'
                st.markdown(href, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- Intent Mode ---
elif mode == "⚙️ Generate Config from Intent":
    st.markdown(f"<div class='card'>", unsafe_allow_html=True)
    st.subheader("Describe Desired Configuration")
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

                # Export as .txt
                b64 = base64.b64encode(result.encode()).decode()
                href = f'<a href="data:file/txt;base64,{b64}" download="generated_config.txt">💾 Download Config as .txt</a>'
                st.markdown(href, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- End main content ---
st.markdown("</div>", unsafe_allow_html=True)
