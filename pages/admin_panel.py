import pandas as pd

from db.db import Database
from frontend.forms import AdminForms
from navigation import make_sidebar
import streamlit as st

make_sidebar()

db = Database()
user_name = st.session_state.get("LOGGED_USER")
user_data = db.get_user_details(user_name)


def admin_panel():
    admin_forms = AdminForms()
    st.title("User Data")
    users_data = db.fetch_all_users_with_passwords()

    df = pd.DataFrame.from_records([user.__dict__ for user in users_data])
    st.dataframe(df)
    st.warning("Warning, superuser mode")
    if st.checkbox("I accept responsibility and understand this mode can be used to initialise and make changes to the authentication database"):
        st.write("You are now in superuser mode")
        st.write("")

        col_1, col_2 = st.columns(2)
        st.session_state.update(user_changed=True)
        with col_1:
            admin_forms.change_user_role()

        st.write("")
        st.write("")

        with col_2:
            admin_forms.change_user_password()
        st.write("")
        st.write("")
        st.write("")
        admin_forms.delete_user()







if st.session_state.get('ROLE') == 'admin':
    admin_panel()

