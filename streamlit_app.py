import streamlit as st
from time import sleep

from db.db import init_db
from navigation import make_sidebar
from widgets import __login__


init_db()

st.title("Welcome to Diamond Corp")

__login__obj = __login__(logout_button_name = 'Logout')

LOGGED_IN = __login__obj.build_login_ui()

st.session_state["LOGIN_OBJ"] = __login__obj

make_sidebar()

