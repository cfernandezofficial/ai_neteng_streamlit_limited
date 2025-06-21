import streamlit as st
from prompts import analyze_cli_output, generate_config_from_intent
import os
import base64

# --- Page config ---
st.set_page_config(page_title="Nexthop AI", layout="wide")

# --- State setup ---
if "show_sidebar" not in st.session_state:
    st.session_state.show_sidebar = False
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "current_section" not in st.session_state:
    st.session_state.current_section = "chat"
if "usage_count" not in st.session_state:
    st.session_state.usage_count = 0

# --- Styling ---
base_bg = "#F9FAFB"  # Neutral light background
text_color = "#1F2937"  # Dark gray for text
card_bg = "white"
primary_color = "#1E3A8A"  # Professional blue accent
border_color = "#E5E7EB"

st.markdown(f"""
    <style>
        html, body {{
            background-color: {base_bg};
            color: {text_color};
            font-family: 'Inter', sans-serif;
            margin: 0;
            padding: 0;
        }}

        header, footer {{visibility: hidden;}}

        .sidebar {{
            position: fixed;
            top: 0;
            left: 0;
            height: 100vh;
            width: 260px;
            background-color: {card_bg};
            border-right: 1px solid {border_color};
            padding: 20px 16px;
            transform: translateX({ '0' if st.session_state.show_sidebar else '-100%' });
            transition: transform 0.3s ease;
            z-index: 1000;
            box-shadow: 2px 0 5px rgba(0,0,0,0.1);
        }}

        .sidebar a {{
            text-decoration: none;
            color: {text_color};
            font-size: 16px;
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 0;
            transition: color 0.2s;
        }}

        .sidebar a:hover {{
            color: {primary_color};
            font-weight: 500;
        }}

        .sidebar input {{
            width: 100%;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid {border_color};
            margin-top: 20px;
            font-size: 14px;
        }}

        .main-area {{
            padding: 60px 40px;
            max-width: 1200px;
            margin: 0 auto;
        }}

        .toggle-btn {{
            position: fixed;
            top: 20px;
            left: 20px;
            font-size: 24px;
            background: {card_bg};
            border: 1px solid {border_color};
            border-radius: 50%;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1100;
            cursor: pointer;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        .card {{
            background-color: {card_bg};
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            margin-bottom: 30px;
            color: {text_color};
        }}

        .chat-box {{
            background-color: {card_bg};
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            margin: 20px 0;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }}

        .chat-box input {{
            width: 100%;
            padding: 12px;
            border-radius: 8px;
            border: 1px solid {border_color};
            font-size: 16px;
            background-color: #F9FAFB;
        }}

        .chat-options button {{
            margin: 8px 8px 0 0;
            padding: 12px 20px;
            border-radius: 999px;
            border: 1px solid {border_color};
            background-color: {card_bg};
            cursor: pointer;
            font-weight: 500;
            transition: background-color 0.2s;
        }}

        .chat-options button:hover {{
            background-color: {primary_color};
            color: white;
            border-color: {primary_color};
        }}

        .stRadio > div {{
            justify-content: center;
            gap: 20px;
        }}

        .stButton > button {{
            background-color: {primary_color};
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-weight: 500;
        }}

        .stButton > button:hover {{
            background-color: #1E40AF;
        }}
    </style>
""", unsafe_allow_html=True)

# --- Toggle Button ---
st.markdown("""
    <div class="toggle-btn" onclick="document.dispatchEvent(new CustomEvent('toggleSidebar'))">☰</div>
""", unsafe_allow_html=True)

# --- Sidebar Navigation ---
st.markdown(f"""
    <div class="sidebar">
        <img src="https://raw.githubusercontent.com/cfernandezofficial/ai_neteng_streamlit_limited/main/logo.png" width="140" style="margin-bottom: 20px;">
        <input type="text" placeholder="Search (Ctrl+K)">
        <a href="#">💬 Chat</a>
        <a href="#">📁 Workspaces</a>
        <a href="#">🕘 History</a>
    </div>
""", unsafe_allow_html=True)

# --- JS Handler ---
st.markdown("""
<script>
    const streamlitEventHandler = () => {
        const sidebarVisible = Streamlit.getSessionState()["show_sidebar"];
        Streamlit.setComponentValue("show_sidebar", !sidebarVisible);
        Streamlit.rerun();
    };

    document.addEventListener("toggleSidebar", streamlitEventHandler);
</script>
""", unsafe_allow_html=True)

# --- Main content starts ---
st.markdown("<div class='main-area'>", unsafe_allow_html=True)

# --- Dark Mode Toggle ---
if st.toggle("🌓 Dark Mode", value=st.session_state.dark_mode):
    st.session_state.dark_mode = True
else:
    st.session_state.dark_mode = False

# --- Usage Notice ---
st.markdown(f"""
<div class='card'>
    <strong>Usage Notice:</strong> Free tier allows up to <strong>5 prompts per session</strong>. <em>({st.session_state.usage_count}/5 used)</em>
</div>
""", unsafe_allow_html=True)

# --- Chat Box ---
st.markdown("""
    <div class='chat-box'>
        <input type='text' placeholder='Paste CLI Output or Upload Config File' disabled>
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
    cli_text = st.text_area("Paste output here (e.g., show run, show ip bgp):", height=300)
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
                href = f'<a href="data:file/txt;base64,{b64}" download="analysis.txt" style="color: {primary_color}; text-decoration: none;">💾 Download Analysis</a>'
                st.markdown(href, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- Intent Mode ---
elif mode == "⚙️ Generate Config from Intent":
    st.markdown(f"<div class='card'>", unsafe_allow_html=True)
    st.subheader("Describe Desired Configuration")
    intent = st.text_area("Example: 'Configure dual-WAN with BGP failover and VRFs'", height=250)

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
                href = f'<a href="data:file/txt;base64,{b64}" download="generated_config.txt" style="color: {primary_color}; text-decoration: none;">💾 Download Config</a>'
                st.markdown(href, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- End main content ---
st.markdown("</div>", unsafe_allow_html=True)