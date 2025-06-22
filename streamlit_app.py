from supabase import create_client
import streamlit as st

# Setup Supabase
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# Logo and Title
st.image("https://raw.githubusercontent.com/cfernandezofficial/ai_neteng_streamlit_limited/main/logo.png", width=400)
st.header("Login")

# --- Login Section ---
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Sign In"):
    try:
        user = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if user.user is not None:
            st.session_state.user = user.user
            st.session_state.authenticated = True
            st.success("✅ Logged in successfully.")
            st.rerun()
        else:
            st.warning("❌ Login failed. Please check your credentials.")
    except Exception as e:
        st.error(f"❌ Login failed: {e}")

# --- Divider ---
st.markdown("---")
st.subheader("Register")

# --- Register Section ---
reg_email = st.text_input("New Email", key="reg_email")
reg_password = st.text_input("New Password", type="password", key="reg_password")

if st.button("Register"):
    try:
        user = supabase.auth.sign_up({"email": reg_email, "password": reg_password})
        if user.user is not None:
            st.success("🎉 Registration successful! Please check your email to confirm.")
        else:
            st.warning("⚠️ Registration failed. Try a different email.")
    except Exception as e:
        st.error(f"❌ Registration failed: {e}")
