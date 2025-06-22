from supabase import create_client
import streamlit as st

# Setup Supabase
supabase = create_client(st.secrets["https://bxmxfumbfsxnkzghubkk.supabase.co"], st.secrets["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ4bXhmdW1iZnN4bmt6Z2h1YmtrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA1NDkxODYsImV4cCI6MjA2NjEyNTE4Nn0.aasae_hSyqM6vGxovCYrRLQ4q3O7m5mxKftszfsNBsA"])

# Login form
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Sign In / Register"):
    try:
        # Try signing in
        user = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if user.user is not None:
            st.session_state.user = user.user
            st.session_state.authenticated = True
            st.success("✅ Logged in! Navigate to the app 👉 from the sidebar.")
            st.experimental_rerun()
        else:
            st.warning("😕 Login failed. Please check your credentials.")
    except Exception as login_error:
        # If login fails, try to sign up
        try:
            signup = supabase.auth.sign_up({"email": email, "password": password})
            st.success("🆕 Account created. Please log in.")
        except Exception as signup_error:
            st.error("🚫 Unable to register. Email may already be used.")

