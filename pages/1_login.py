import streamlit as st
from supabase import create_client

# --- Display Logo at Top ---
st.image("logo.png", width=300)  # Make sure 'logo.png' is in the root folder or adjust path

# --- Supabase Setup ---
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# --- Login/Register UI ---
email = st.text_input("Email")
password = st.text_input("Password", type="password")

col1, col2 = st.columns(2)

# --- LOGIN Button ---
with col1:
    if st.button("🔓 Login"):
        try:
            user = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            if user.user is not None:
                st.session_state.user = user.user
                st.session_state.authenticated = True
                st.success("✅ Logged in successfully.")
                st.experimental_rerun()
            else:
                st.error("❌ Login failed. Invalid credentials.")
        except Exception as e:
            st.error(f"❌ Login failed: {e}")

# --- REGISTER Button ---
with col2:
    if st.button("🆕 Register"):
        try:
            user = supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            st.success("🎉 Account created! Now click 'Login' to sign in.")
        except Exception as e:
            st.error("🚫 Unable to register. Email may already be used.")
