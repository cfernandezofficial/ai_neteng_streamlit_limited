import streamlit as st
from supabase import create_client

# Setup Supabase
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# Login form
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Sign In / Register"):
    try:
        user = supabase.auth.sign_in_with_password({"email": email, "password": password})
        st.session_state.user = user.user
        st.session_state.authenticated = True
        st.success("✅ Logged in! Navigate to the app 👉 from the sidebar.")
        st.experimental_rerun()  # optional to refresh session state
    except Exception:
        supabase.auth.sign_up({"email": email, "password": password})
        st.success("🆕 Account created. Please log in.")

