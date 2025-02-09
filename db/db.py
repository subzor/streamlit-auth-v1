import hashlib
import os

import streamlit as st
from streamlit.runtime.secrets import Secrets

from frontend.widgets import SecretsPage
from src.consts import Paths
from src.models import UserDetails
from src.utils import non_empty_str_check
import psycopg2


class Database:
    connection: psycopg2.extensions.connection

    def __init__(self):
        self.secrets_page = SecretsPage()
        self.config = self._get_secrets_config()
        self.config_check = False
        if self.config:
            self.config_check = self._check_config()
            if self.config_check:
                self.connection_string = (f"host='{self.config.host}' port='{self.config.port}' dbname='{self.config.database}' "
                                          f"user='{self.config.username}' password='{self.config.password}'")

    def connect(self):
        try:
            self.connection = psycopg2.connect(self.connection_string)
            return True
        except psycopg2.Error:
            st.error(f"Connection error. Please check your secrets.")
            self.secrets_page.secrets_widget()
            return False

    def _check_config(self) -> bool:
        try:
            if not (self.config.host and self.config.port and self.config.database and self.config.username and self.config.password):
                return False
        except AttributeError:
            st.error("Missing secrets. Read the README.md file for more information.")
            self.secrets_page.secrets_widget()
            return False
        return True

    @staticmethod
    def _get_secrets_config():
        try:
            _config = st.secrets.connections["postgresql"]
        except AttributeError:
            st.secrets = Secrets()
            st.error("The secrets file structure is incorrect. Read the README.md file for more information.")
            if st.button("Clear secrets file? This will delete all secrets"):
                os.remove(Paths.SECRETS_FILE)
                st.rerun()
            return None
        return _config



    @staticmethod
    def hash_password(password) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def table_exists(self, table_name) -> bool:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table_name}');")
                result = cursor.fetchone()
            return result[0]

        except psycopg2.Error as e:
            st.error(f"table_exists: {e}")
            return False
    
    def create_users_table(self) -> None:
        create_table_query = '''CREATE TABLE IF NOT EXISTS users
                                (id SERIAL PRIMARY KEY,
                                email TEXT NOT NULL UNIQUE,
                                name TEXT NOT NULL,
                                username TEXT NOT NULL UNIQUE,
                                password TEXT NOT NULL,
                                role TEXT NOT NULL);'''
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(create_table_query)
        except psycopg2.Error as e:
            st.error(f"create_users_table: {e}")
    
    def ensure_admin_exists(self) -> None:
        try:
            admin_exist = self.get_user_details("admin")
            if not admin_exist:
                admin_email = "admin@admin.pl"
                admin_name = "Admin"
                admin_username = "admin"
                admin_password = self.hash_password("admin123@")
                self.add_user_to_db(admin_email, admin_name, admin_username, admin_password, role='admin')
                return
            if admin_exist.role != "admin":
                self.edit_user_role("admin", "admin")
        except psycopg2.Error as e:
            st.error(f"ensure_admin_exists: {e}")
    
    def init_db(self) -> None:
        if not self.table_exists('users'):
            self.create_users_table()
        self.ensure_admin_exists()

    def add_user_to_db(self, email, name, username, password, role='user') -> bool:
        hashed_pwd = self.hash_password(password)
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"INSERT INTO users (email, name, username, password, role) "
                            f"VALUES ('{email}', '{name}', '{username}', '{hashed_pwd}', '{role}')"
                    )
                self.connection.commit()
                return True
        except psycopg2.Error as e:
            st.error(f"Add user: {e}")
            return False

    def check_email_in_db(self, email) -> bool:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT email FROM users WHERE email = '{email}'")
                result = cursor.fetchone()
            return bool(result)
        except psycopg2.Error as e:
            st.error(f"unique_email_in_db {e}")
        return True

    def check_user_in_db(self, username) -> bool | None:
        if not non_empty_str_check(username):
            return None
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT username FROM users WHERE username = '{username}'")
                result = cursor.fetchone()
            return bool(result)
        except psycopg2.Error as e:
            st.error(f"check_user_in_db {e}")
        return True

    def get_user_role(self, username) -> str | None:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT role FROM users WHERE username = '{username}'")
                result = cursor.fetchone()
            return result[0] if result else None
        except psycopg2.Error as e:
            st.error(f"get_user_role {e}")

    def verify_user(self, username: str, password: str) -> tuple[bool, str | None]:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT password, role FROM users WHERE username = '{username}'")
                result = cursor.fetchone()
            if result:
                stored_hashed_password, role = result
                if stored_hashed_password == self.hash_password(password):
                    return True, role
            return False, None
        except psycopg2.Error as e:
            st.error(f"verify_user{e}")
            return False, None

    def fetch_all_users_with_passwords(self) -> list:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users")
                users = cursor.fetchall()
                users = [UserDetails(*user) for user in users]
            return users
        except psycopg2.Error as e:
            st.error(f"fetch_all_users_with_passwords{e}")
            return []

    def edit_user_role(self, username, role) -> bool:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"UPDATE users SET role = '{role}' WHERE username = '{username}'")
                self.connection.commit()
            return True
        except psycopg2.Error as e:
            st.error(f"edit_user_role{e}")
            return False

    def delete_user(self, username) -> bool:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"DELETE FROM users WHERE username = '{username}'")
                self.connection.commit()
            return True
        except psycopg2.Error as e:
            st.error(f"delete_user{e}")
            return False

    def update_password(self, username, password) -> bool:
        hashed_pwd = self.hash_password(password)
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"UPDATE users SET password = '{hashed_pwd}' WHERE username = '{username}'")
                self.connection.commit()
            return True
        except psycopg2.Error as e:
            st.error(f"update_password{e}")
            return False

    def update_email(self, username, email) -> bool:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"UPDATE users SET email = '{email}' WHERE username = '{username}'")
                self.connection.commit()
            return True
        except psycopg2.Error as e:
            st.error(f"update_email{e}")
            return False

    def update_name(self, username, name) -> bool:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"UPDATE users SET name = '{name}' WHERE username = '{username}'")
                self.connection.commit()
            return True
        except psycopg2.Error as e:
            st.error(f"update_name {e}")
            return False

    def get_user_details(self, username) -> UserDetails | None:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT id, email, name, username, password, role FROM users WHERE username = '{username}'")
                result = cursor.fetchone()
            if not result:
                return None
            data = UserDetails(*result)
            return data
        except psycopg2.Error as e:
            st.error(f"get_user_details{e}")
            return None

    def get_all_users(self) -> list:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT username FROM users")
                users = cursor.fetchall()
                users = [user[0] for user in users]
            return users
        except Exception as e:
            st.error(f"get_all_users {e}")
            return []


def get_logged_user_details():
    """
    Returns the logged in user's details.
    """
    db = st.session_state.get("DB")
    try:
        details = db.get_user_details(st.session_state.get("LOGGED_USER"))
        return details
    except AttributeError:
        pass
