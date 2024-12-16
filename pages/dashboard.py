from db.db import Database
from navigation import make_sidebar
import streamlit as st

make_sidebar()

db = Database()
user_name = st.session_state.get("LOGGED_USER")
user_details = db.get_user_details(user_name)

st.write(
    f"""
# 🕵️ Secret Company Stuff

This is a secret page that only logged-in users can see.

Don't tell anyone.

For real.

Your user data: 

"""
)
for s, d in user_details.__dict__.items():
    st.write(f"{s.capitalize()}: {d} ")

