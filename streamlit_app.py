import streamlit as st

from db.db import Database
from navigation import make_sidebar
from widgets import __login__

db = Database()
db.init_db()

st.title("Welcome to Diamond Corp")

__login__obj = __login__(logout_button_name = 'Logout')

LOGGED_IN = __login__obj.build_login_ui()

st.session_state["LOGIN_OBJ"] = __login__obj

make_sidebar()

if LOGGED_IN:
    st.switch_page("pages/dashboard.py")

