import streamlit as st
from supabase import create_client

# ✅ Load Supabase credentials from Streamlit secrets
SUPABASE_URL = st.secrets["https://bxmxfumbfsxnkzghubkk.supabase.co"]
SUPABASE_KEY = st.secrets["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ4bXhmdW1iZnN4bmt6Z2h1YmtrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA1NDkxODYsImV4cCI6MjA2NjEyNTE4Nn0.aasae_hSyqM6vGxovCYrRLQ4q3O7m5mxKftszfsNBsA"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ✅ Clean login UI
st.title("🔐 Login / Register")
email = st.text_input("Email")
password = st.text_input("Password", type="password")

# ✅ Handle login or signup
if st.button("Sign In / Register"):
    try:
        # Try to sign in
        user = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if user.user is not None:
            st.session_state.user = user.user
            st.session_state.authenticated = True
            st.success("✅ Logged in! Navigate to the app 👉 from the sidebar.")
            st.experimental_rerun()
        else:
            st.warning("😕 Login failed. Please check your credentials.")
    except Exception:
        try:
            # Try to register if login fails
            supabase.auth.sign_up({"email": email, "password": password})
            st.success("🆕 Account created. Please log in.")
        except Exception:
            st.error("🚫 Unable to register. Email may already be used or invalid.")

# ✅ Optional: Hide sidebar on login page for cleaner UX
st.markdown("""
    <style>
    section[data-testid="stSidebar"] { display: none; }
    </style>
""", unsafe_allow_html=True)