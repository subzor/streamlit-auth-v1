import pandas as pd

from db.db import Database
from navigation import make_sidebar
import streamlit as st

make_sidebar()


def admin_panel():
    st.warning("Warning, superuser mode")
    if st.checkbox("I accept responsibility and understand this mode can be used to initialise and make changes to the authentication database"):
        st.write("You are now in superuser mode")


st.write(f'Welcome to the {st.session_state.get("ROLE")} page!')
if st.session_state.get('ROLE') == 'admin':
    st.title("User Data")
    db = Database()
    user_data = db.fetch_all_users_with_passwords()
    df = pd.DataFrame(user_data, columns=["Email", "Name", "Username", "Password", "Role"])
    st.dataframe(df)

else:
    st.write("You do not have permission to view data from this page.")