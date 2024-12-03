from navigation import make_sidebar
import streamlit as st

make_sidebar()

st.write(
    f"""
# 🔓 Secret Company Stuff

This is a secret page that only logged-in users can see.

Don't tell anyone.

For real.

Your username is: `{st.session_state.get("LOGGED_USER")}`

"""
)
