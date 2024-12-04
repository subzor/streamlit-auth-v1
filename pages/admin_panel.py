import pandas as pd

from db.db import Database
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

        st.title("User Data")
        users_data = db.fetch_all_users_with_passwords()
        df = pd.DataFrame(users_data, columns=["Email", "Name", "Username", "Password", "Role"])
        st.dataframe(df)


        st.markdown


        with st.form("Change user password"):
            st.write("Change user password")
            usr_name = st.text_input("Username")
            new_password = st.text_input("New password", type="password")
            if st.form_submit_button("Change password"):
                response = db.update_password(usr_name, new_password)
                if response:
                    st.write("Password changed successfully! :sunglasses:")
                else:
                    st.error("Error changing password")





if st.session_state.get('ROLE') == 'admin':
    admin_panel()

