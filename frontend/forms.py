from db.db import Database
import streamlit as st


db = Database()
user_name = st.session_state.get("LOGGED_USER")
user_data = db.get_user_details(user_name)

def change_password_form():
    with st.form("Change password", clear_on_submit=True):

        col_1, col_2, col_3 = st.columns(3)

        st.write("")
        st.write("")

        old_password = col_1.text_input("Old password", placeholder="Old password", type="password")
        new_password = col_2.text_input("New password", placeholder="New password", type="password")
        confirm_password = col_3.text_input("Confirm password", placeholder="Confirm password", type="password")
        if st.form_submit_button("Change password"):
            if new_password == confirm_password and new_password != "":

                authenticate_user_check, _ = db.verify_user(user_name, old_password)
                if authenticate_user_check:
                    if old_password != new_password:
                        response = db.update_password(user_name, new_password)
                        if response:
                            st.write("Password changed successfully! :sunglasses:")
                        else:
                            st.error("Error changing password")
                    else:
                        st.warning("New password cannot be the same as the old password")
                else:
                    st.error("Wrong old password!")
            else:
                st.warning("Passwords do not match")

def change_name_form():
    with st.form("Change name", clear_on_submit=True):
        st.write("")
        st.write(f"Old name: {user_data["name"]}")
        new_name = st.text_input("New name", value="")
        password = st.text_input("Password", type="password", value="")

        if st.form_submit_button("Change name"):
            if new_name != "" or password != "":

                authenticate_user_check, _ = db.verify_user(user_name, password)
                if authenticate_user_check:
                    response = db.update_name(user_name, new_name)
                    if response:
                        st.write("Name changed successfully! :sunglasses:")
                    else:
                        st.error("Error changing name")
                else:
                    st.warning("Wrong password!")
            else:
                st.warning("Name and password cannot be empty")


def change_email_form():
    with st.form("Change email", clear_on_submit=True):
        st.write("")
        st.write(f"Old email: {user_data["email"]}")
        new_email = st.text_input("New email", value="")
        password = st.text_input("Password", type="password", value="")

        if st.form_submit_button("Change email"):
            if new_email != "" or password != "":
                authenticate_user_check, _ = db.verify_user(user_name, password)
                if authenticate_user_check:
                    response = db.update_email(user_name, new_email)
                    if response:
                        st.write("Email changed successfully! :sunglasses:")
                    else:
                        st.error("Error changing email")
                else:
                    st.warning("Wrong password!")
            else:
                st.warning("Email and password cannot be empty")