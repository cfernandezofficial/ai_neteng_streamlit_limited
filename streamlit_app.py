import streamlit as st

# Set page config
st.set_page_config(
    page_title="NextHop AI",
    page_icon="🌐",
    layout="wide"
)

# Custom CSS to style the page
st.markdown("""
    <style>
        body {
            background-color: #f9f9fb;
        }
        .main-title {
            font-size: 3.5rem;
            font-weight: 800;
            line-height: 1.2;
        }
        .highlight {
            color: #C026D3;
        }
        .sub-text {
            font-size: 1.1rem;
            color: #444;
            margin-top: 1rem;
        }
        .try-button {
            background-color: white;
            border: 1px solid #ccc;
            padding: 0.75rem 1.5rem;
            border-radius: 10px;
            font-weight: bold;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            margin-top: 2rem;
        }
        .try-button:hover {
            background-color: #f0f0f0;
        }
        .container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 3rem;
        }
        .left {
            flex: 1;
            padding-right: 2rem;
        }
        .right {
            flex: 1;
        }
        .right img {
            width: 100%;
            border-radius: 1rem;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        }
    </style>
""", unsafe_allow_html=True)

# Page layout
st.markdown("""
    <div class="container">
        <div class="left">
            <h1 class="main-title">
                <span class="highlight">NextHop AI</span> – Your AI Assistant for Network Engineering
            </h1>
            <p class="sub-text">
                Analyze, generate, and streamline configurations with AI-powered tools built for modern network engineers.
            </p>
            <a href="https://nexthopai.streamlit.app/" class="try-button">Try Now →</a>
        </div>
        <div class="right">
            <img src="https://raw.githubusercontent.com/cfernandezofficial/ai_neteng_streamlit_limited/main/logo.png" alt="Hero Image">
        </div>
    </div>
""", unsafe_allow_html=True)
