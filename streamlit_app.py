from supabase import create_client
import streamlit as st

# Setup Supabase
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# Login form
st.image("https://raw.githubusercontent.com/cfernandezofficial/ai_neteng_streamlit_limited/main/logo.png", width=200)
st.header("🔐 Login")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Sign In"):
    try:
        user = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if user.user is not None:
            st.session_state.user = user.user
            st.session_state.authenticated = True
            st.success("✅ Logged in successfully.")
            st.rerun()  # ✅ Replaces the old experimental_rerun
        else:
            st.warning("❌ Login failed. Please check your credentials.")
    except Exception as e:
        st.error(f"❌ Login failed: {e}")
