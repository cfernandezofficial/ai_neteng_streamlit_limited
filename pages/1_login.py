from supabase import create_client
import streamlit as st

# Setup Supabase using proper keys from secrets
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Login form
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Sign In / Register"):
    try:
        user = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if user.user is not None:
            st.session_state.user = user.user
            st.session_state.authenticated = True
            st.success("✅ Logged in! Navigate to the app 👉 from the sidebar.")
            st.experimental_rerun()
        else:
            st.warning("😕 Login failed. Please check your credentials.")
    except Exception as login_error:
        try:
            signup = supabase.auth.sign_up({"email": email, "password": password})
            st.success("🆕 Account created. Please log in.")
        except Exception as signup_error:
            st.error("🚫 Unable to register. Email may already be used.")
