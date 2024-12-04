import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages


def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]


def make_sidebar():
    with st.sidebar:
        st.title("💎 Sub Corp")
        st.write("")
        st.write("")

        if st.session_state.get("LOGGED_IN", False):
            st.page_link("streamlit_app.py", label="Start", icon="🏠")
            st.page_link("pages/dashboard.py", label="Dashboard", icon="🕵️")
            st.page_link("pages/settings.py", label="Settings", icon="🔒")

            st.write("")
            st.write("")
            st.session_state.get("LOGIN_OBJ").logout_widget()

        elif get_current_page_name() != "streamlit_app":
            # If anyone tries to access a secret page without being logged in,
            # redirect them to the login page
            st.switch_page("streamlit_app.py")

