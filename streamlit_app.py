import streamlit as st

# Configure the page
st.set_page_config(page_title="NextHop AI", layout="wide")

# ---- Header ----
with st.container():
    cols = st.columns([1, 6, 3])
    with cols[0]:
        st.image("https://via.placeholder.com/25x25", width=25)
    with cols[1]:
        st.markdown("### NextHop AI")
    with cols[2]:
        st.markdown("<div style='text-align: right;'>"
                    "<a href='#'>Home</a> &nbsp;&nbsp;&nbsp; "
                    "<a href='#'>Tools</a> &nbsp;&nbsp;&nbsp; "
                    "<a href='#'>Pricing</a>"
                    "</div>", unsafe_allow_html=True)

st.markdown("---")

# ---- Hero Section ----
with st.container():
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("<h1 style='font-size: 42px;'>"
                    "<span style='color:#ec4899;'>NextHop AI</span> – Your AI Assistant for Network Engineering"
                    "</h1>", unsafe_allow_html=True)
        st.markdown("Analyze, generate, and streamline configurations with AI-powered tools built for modern network engineers.")
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("Try Now")

    with col2:
        st.image("https://images.unsplash.com/photo-1556742044-3c52d6e88c62", caption="AI Engineer")