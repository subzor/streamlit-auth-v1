import time

import streamlit as st

from db.db import Database
from navigation import make_sidebar
from widgets import LoginPage

db = Database()
db.init_db()

st.title("Welcome to Sub Corp")

login_page = LoginPage(logout_button_name ='Logout')

login_page.build_login_ui()

st.session_state["LOGIN_OBJ"] = login_page

make_sidebar()




