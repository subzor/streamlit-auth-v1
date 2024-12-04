
import pandas as pd

from db.db import Database
from frontend.forms import change_password_form, change_name_form, change_email_form
from navigation import make_sidebar
import streamlit as st

make_sidebar()

db = Database()
user_name = st.session_state.get("LOGGED_USER")
user_data = db.get_user_details(user_name)

def admin_panel():
    st.warning("Warning, superuser mode")
    if st.checkbox("I accept responsibility and understand this mode can be used to initialise and make changes to the authentication database"):
        st.write("You are now in superuser mode")


def user_panel():

    change_password_form()
    change_name_form()
    change_email_form()

st.write(f"""
# 🔓 Settings
""")

if st.session_state.get('ROLE') == 'admin':
    st.title("User Data")

    user_data = db.fetch_all_users_with_passwords()
    df = pd.DataFrame(user_data, columns=["Email", "Name", "Username", "Password", "Role"])
    st.dataframe(df)

    # ss = db.update_password("daniel", "daniel123")
    # st.write(ss)

else:
    user_panel()