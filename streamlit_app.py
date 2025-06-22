import streamlit as st
from supabase import create_client

# --- Display Logo ---
st.image("https://raw.githubusercontent.com/cfernandezofficial/ai_neteng_streamlit_limited/main/logo.png", width=280)

# --- Setup Supabase ---
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# --- Form Inputs ---
email = st.text_input("Email")
password = st.text_input("Password", type="password")

# --- Columns for Buttons ---
col1, col2 = st.columns(2)

# --- LOGIN Button ---
with col1:
    if st.button("Login"):
        try:
            user = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            if user.user is not None:
                st.session_state.user = user.user
                st.session_state.authenticated = True
                st.success("✅ Logged in successfully.")
                st.rerun()
            else:
                st.error("❌ Login failed. Invalid credentials.")
        except Exception as e:
            st.error(f"❌ Login failed: {e}")

# --- REGISTER Button ---
with col2:
    if st.button("Register"):
        try:
            user = supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            st.success("🎉 Account created! Please log in.")
        except Exception as e:
            st.error("🚫 Registration failed. Email may already be used.")
