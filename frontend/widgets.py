from time import sleep

import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_cookies_manager import EncryptedCookieManager

from db.db import Database
from src.utils import check_valid_name, check_valid_email, validate_password


class LoginPage:
    """
    Builds the UI for the Login/ Sign Up page.
    """

    def __init__(self, logout_button_name: str = 'Logout'):
        """
        Arguments:
        -----------
        1. logout_button_name : The logout button name.
        """
        self.logout_button_name = logout_button_name
        self.db = Database()

        self.cookies = EncryptedCookieManager(
        prefix="streamlit_login_ui_yummy_cookies",
        password='9d68d6f2-4258-45c9-96eb-2d6bc74ddbb5-d8f49cab-edbb-404a-94d0-b25b1d4a564b_123123_asdas12')

        if not self.cookies.ready():
            st.stop()   

    def login_widget(self) -> None:
        """
        Creates the login widget, checks and sets cookies, authenticates the users.
        """

        # Checks if cookie exists.
        if not st.session_state['LOGGED_IN']:
            if not st.session_state['LOGOUT_BUTTON_HIT']:
                fetched_cookies = self.cookies
                if '__streamlit_login_signup_ui_username__' in fetched_cookies.keys():
                    if fetched_cookies['__streamlit_login_signup_ui_username__'] != '1c9a923f-fb21-4a91-b3f3-5f18e3f01182':
                        st.session_state['LOGGED_IN'] = True
                        st.session_state['LOGGED_USER'] = self.cookies.get('__streamlit_login_signup_ui_username__')
                        st.session_state['ROLE'] = self.db.get_user_role(st.session_state['LOGGED_USER'])


        if not st.session_state['LOGGED_IN']:
            st.session_state['LOGOUT_BUTTON_HIT'] = False 

            del_login = st.empty()
            with del_login.form("Login Form"):
                username = st.text_input("Username", placeholder = 'Your unique username')
                password = st.text_input("Password", placeholder = 'Your password', type = 'password')

                st.markdown("###")
                login_submit_button = st.form_submit_button(label = 'Login')

                if login_submit_button:
                    authenticate_user_check, role = self.db.verify_user(username, password)

                    if not authenticate_user_check:
                        st.error("Invalid Username or Password!")

                    else:
                        st.session_state['LOGGED_IN'] = True
                        st.session_state['ROLE'] = role
                        st.session_state['LOGGED_USER'] = username
                        self.cookies['__streamlit_login_signup_ui_username__'] = username
                        self.cookies.save()
                        del_login.empty()
                        st.rerun()

    def sign_up_widget(self) -> None:
        """
        Creates the sign-up widget and stores the user info in a secure way in the users.db file.
        """
        with st.form("Sign Up Form"):
            name_sign_up = st.text_input("Name *", placeholder = 'Please enter your name')
            valid_name_check = check_valid_name(name_sign_up)

            email_sign_up = st.text_input("Email *", placeholder = 'Please enter your email')
            valid_email_check = check_valid_email(email_sign_up)
            unique_email_check = self.db.unique_email_in_db(email_sign_up)
            
            username_sign_up = st.text_input("Username *", placeholder = 'Enter a unique username')
            unique_username_check = self.db.check_user_in_db(username_sign_up)

            password_sign_up = st.text_input("Password *", placeholder = 'Create a strong password', type = 'password')
            strong_password = validate_password(password_sign_up)
            st.markdown("###")
            sign_up_submit_button = st.form_submit_button(label = 'Register')

            if sign_up_submit_button:
                if not valid_name_check:
                    st.error("Please enter a valid name!")

                elif not valid_email_check:
                    st.error("Please enter a valid Email!")
                
                elif not unique_email_check:
                    st.error("Email already exists!")

                elif unique_username_check is None:
                    st.error('Please enter a non - empty Username!')

                elif not unique_username_check:
                    st.error(f'Sorry, username {username_sign_up} already exists!')

                elif not strong_password:
                    st.error('Password should be at least 8 characters long and should contain at least one uppercase letter, one lowercase letter, one digit and one special character.')

                if valid_name_check and valid_email_check and unique_email_check and unique_username_check and strong_password:
                    self.db.add_user_to_db(email=email_sign_up,
                                   name=name_sign_up,
                                   username=username_sign_up,
                                   password=password_sign_up)
                    st.success("Registration Successful!")
                    sleep(2)

    def logout_widget(self) -> None:
        """
        Creates the logout widget in the sidebar only if the user is logged in.
        """
        if st.session_state['LOGGED_IN']:
            del_logout = st.sidebar.empty()
            del_logout.markdown("#")
            logout_click_check = del_logout.button(self.logout_button_name)

            if logout_click_check:
                st.session_state['LOGOUT_BUTTON_HIT'] = True
                st.session_state['LOGGED_IN'] = False
                st.session_state.update({'LOGGED_USER': None})
                st.session_state.update({'ROLE': None})
                self.cookies['__streamlit_login_signup_ui_username__'] = '1c9a923f-fb21-4a91-b3f3-5f18e3f01182'
                self.cookies.save()
                del_logout.empty()
                st.rerun()

    def nav_sidebar(self):
        """
        Creates the side navigation bar
        """
        main_page_sidebar = st.sidebar.empty()
        with main_page_sidebar:
            selected_option = option_menu(
                menu_title = 'Navigation',
                menu_icon = 'list-columns-reverse',
                icons = ['box-arrow-in-right', 'person-plus', 'x-circle','arrow-counterclockwise'],
                options = ['Login', 'Create Account'],
                styles = {
                    "container": {"padding": "5px"},
                    "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px"}},
                key='nav'
                )

        return main_page_sidebar, selected_option

    def build_login_ui(self):
        """
        Brings everything together, calls important functions.
        """

        if 'LOGGED_IN' not in st.session_state:
            st.session_state['LOGGED_IN'] = False

        if 'LOGOUT_BUTTON_HIT' not in st.session_state:
            st.session_state['LOGOUT_BUTTON_HIT'] = False

        main_page_sidebar, selected_option = self.nav_sidebar()

        if selected_option == 'Login':
            self.login_widget()
        
        if selected_option == 'Create Account':
            self.sign_up_widget()

        if st.session_state['LOGGED_IN']:
            main_page_sidebar.empty()

        return st.session_state['LOGGED_IN']



