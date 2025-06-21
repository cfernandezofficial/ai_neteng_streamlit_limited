
import streamlit as st
from prompts import analyze_cli_output, generate_config_from_intent
import os

st.set_page_config(page_title="AI Network Engineer Assistant", layout="wide")
st.image("logo.png", width=120)
# Branded Header Section
st.markdown("""
<div style='text-align: center; padding: 1rem 0;'>
    <h1 style='font-size: 3em;'>🚀 Nexthop AI</h1>
    <p style='font-size: 1.3em; color: #555;'>Your AI-Powered Network Engineer Assistant</p>
</div>
""", unsafe_allow_html=True)
st.markdown("<hr style='border:1px solid #ccc;'>", unsafe_allow_html=True)

st.title("🤖 AI Network Engineer Assistant")

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

st.info(f"🆓 Free to use – up to {MAX_USES} prompts per session. ({st.session_state.usage_count}/{MAX_USES} used)")

if st.session_state.usage_count >= MAX_USES:
    st.warning("🚫 You've reached the usage limit for this session. Please refresh the page or come back later.")
    st.stop()

mode = st.radio("Select mode:", ["🧠 Analyze CLI/Config", "⚙️ Generate Config from Intent"])

if mode == "🧠 Analyze CLI/Config":
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
