import os

import streamlit as st

from db.db import Database
from navigation import make_sidebar
from frontend.widgets import LoginPage, SecretsPage
from dotenv import load_dotenv

from src.utils import is_secrets_toml_file_exists

load_dotenv()

def main():
    db = Database()

    if db.config_check:
        db_connection = db.connect()
        if db_connection:
            db.init_db()
            st.session_state["DB"] = db
            st.title("Welcome to Sub Corp")

            login_page = LoginPage(logout_button_name ='Logout')

            login_page.build_login_ui()

            st.session_state["LOGIN_OBJ"] = login_page

            make_sidebar()

if is_secrets_toml_file_exists():
    main()
else:
    secrets_page = SecretsPage().secrets_widget()
    st.write("streamlit app is not configured properly")





