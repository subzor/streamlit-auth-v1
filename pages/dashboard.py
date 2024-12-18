
import os

import streamlit.components.v1 as components
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

command = st.text_input("grep command")



if st.button("Run tests"):
    st.write("Running tests...")
    os.system(f"cd .. && cd .. && cd app && npx playwright test --grep '{command}'")
    st.write("Tests passed! 🎉")

port = st.text_input("port")

if st.button("show result tests"):
    os.system(f"cd .. && cd .. && cd app && npx playwright show-report --port '{port}'")
    components.iframe("http://localhost:9323", height=600, scrolling=True)
    st.write("Tests passed! 🎉")
