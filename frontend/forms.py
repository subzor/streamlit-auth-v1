
from time import sleep

from db.db import Database
import streamlit as st

from src.enums import UserRoleType
from src.models import UserDetails


class Forms:

    def __init__(self):
        self.db = Database()
        self.user_name = st.session_state.get("LOGGED_USER")
        self.user_datails: UserDetails = self.db.get_user_details(self.user_name)
        self.users_data = self.db.get_all_users()
        self.users_copy = self.users_data.copy()
        self.users_copy.remove(self.user_name)



class SettingsForms(Forms):

    def change_password_form(self):
        with st.form("Change password", clear_on_submit=True):


            col_1, col_2, col_3 = st.columns(3)
            st.write("")
            st.write("")

            old_password = col_1.text_input("Old password", placeholder="Old password", type="password")
            new_password = col_2.text_input("New password", placeholder="New password", type="password")
            confirm_password = col_3.text_input("Confirm password", placeholder="Confirm password", type="password")
            if st.form_submit_button("Change password"):
                if new_password == confirm_password and new_password != "":
                    authenticate_user_check, _ = self.db.verify_user(self.user_name, old_password)
                    if authenticate_user_check:
                        if old_password != new_password:
                            response = self.db.update_password(self.user_name, new_password)
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

    def change_name_form(self):
        with st.form("Change name", clear_on_submit=True):
            st.write("")
            st.write(f"Old name: {self.user_datails.name}")
            new_name = st.text_input("New name", value="")
            password = st.text_input("Password", type="password", value="")

            if st.form_submit_button("Change name"):
                if new_name != "" or password != "":

                    authenticate_user_check, _ = self.db.verify_user(self.user_name, password)
                    if authenticate_user_check:
                        response = self.db.update_name(self.user_name, new_name)
                        if response:
                            st.write("Name changed successfully! :sunglasses:")
                        else:
                            st.error("Error changing name")
                    else:
                        st.warning("Wrong password!")
                else:
                    st.warning("Name and password cannot be empty")


    def change_email_form(self):
        with st.form("Change email", clear_on_submit=True):
            st.write("")
            st.write(f"Old email: {self.user_datails.email}")
            new_email = st.text_input("New email", value="")
            password = st.text_input("Password", type="password", value="")

            if st.form_submit_button("Change email"):
                if new_email != "" or password != "":
                    authenticate_user_check, _ = self.db.verify_user(self.user_name, password)
                    if authenticate_user_check:
                        response = self.db.update_email(self.user_name, new_email)
                        if response:
                            st.write("Email changed successfully! :sunglasses:")
                        else:
                            st.error("Error changing email")
                    else:
                        st.warning("Wrong password!")
                else:
                    st.warning("Email and password cannot be empty")




class AdminForms(Forms):

    @staticmethod
    def _user_changed():
        st.session_state.selected_role = ""

    def change_user_role(self):
        st.write("Change user role")
        usr_name = st.selectbox("Username", self.users_copy, key="role", on_change=self._user_changed)

        user_roles = [""] + UserRoleType.list()

        new_role = st.selectbox("New role", user_roles, key="selected_role")
        if st.button("Change role"):
            if usr_name and new_role != "":
                response = self.db.edit_user_role(usr_name, new_role)
                if response:
                    st.success("Role changed successfully! :sunglasses:")
                    sleep(2)
                    st.rerun()
                else:
                    st.error("Error changing role")
            else:
                st.warning("Please select user and a role")

    def change_user_password(self):
        st.write("Change user password")
        usr_name = st.selectbox("Username", self.users_copy, key="pass", on_change=lambda: st.session_state.update(user_changed=True))
        new_password = st.text_input("New password", type="password")
        if st.button("Change password"):
            if new_password != "":
                response = self.db.update_password(usr_name, new_password)
                if response:
                    st.success("Password changed successfully! :sunglasses:")
                    sleep(2)
                    st.rerun()
                else:
                    st.error("Error changing password")
            else:
                st.warning("Password cannot be empty")

    def delete_user(self):
        st.write("Delete user")
        usr_name = st.selectbox("Username", self.users_copy, key="del", on_change=lambda: st.session_state.update(user_changed=True))
        col_1, col_2 = st.columns(2)
        with col_1:
            check = st.checkbox("Are you sure?")

        if col_2.button("Delete user"):
            if check and usr_name:
                response = self.db.delete_user(usr_name)
                if response:
                    st.success("User deleted successfully! :sunglasses:")
                    sleep(2)
                    st.rerun()
                else:
                    st.error("Error deleting user")
            else:
                st.warning("Please confirm and select a user to delete")




