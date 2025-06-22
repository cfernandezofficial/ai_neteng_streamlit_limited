from supabase import create_client
import streamlit as st

# Connect to Supabase using secrets (make sure these are set in Streamlit Secrets)
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# UI
st.title("🔐 Login or Register")
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Sign In / Register"):
    try:
        # Try logging in
        user = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if user.user is not None:
            st.session_state.user = user.user
            st.session_state.authenticated = True
            st.session_state.plan = user.user.user_metadata.get("plan", "free")
            st.success(f"✅ Logged in as {email} ({st.session_state.plan} plan)")
            st.experimental_rerun()
        else:
            st.warning("😕 Login failed. Please check your credentials.")
    except Exception:
        # If login fails, try registering new user
        try:
            signup = supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {"plan": "free"}
                }
            })
            st.success("🆕 Account created! Please log in now.")
        except Exception as signup_error:
            st.error("🚫 Unable to register. Email may already be used.")
