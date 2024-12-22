
from navigation import make_sidebar
import streamlit as st

from db.db import get_logged_user_details

make_sidebar()

user_details = get_logged_user_details()

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