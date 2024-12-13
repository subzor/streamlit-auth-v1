
import hashlib
import psycopg2
import streamlit as st

from src.utils import non_empty_str_check


class Database:
    def __init__(self, db_name='users.db'):
        self.db_name = db_name

    def _connect(self):
        return psycopg2.connect(**st.secrets.database)

    def column_exists(self, cursor, table_name, column_name):
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        return any(column[1] == column_name for column in columns)

    def init_db(self):
        # create_table_query
        conn = self._connect()
        create_table_query = '''CREATE TABLE IF NOT EXISTS users
                                (id SERIAL PRIMARY KEY,
                                email TEXT NOT NULL UNIQUE,
                                name TEXT NOT NULL,
                                username TEXT NOT NULL UNIQUE,
                                password TEXT NOT NULL,
                                role TEXT NOT NULL);'''

        try:
            cursor = conn.cursor()
            cursor.execute(create_table_query)
            conn.commit()
        except psycopg2.Error as e:
            st.error(f"Database error: {e}")
        except Exception as e:
            st.error(f"An error occurred: {e}")

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = 'admin'")
            admin_exists = cursor.fetchone()
            if not admin_exists:
                admin_email = "admin@admin.pl"
                admin_name = "Admin"
                admin_username = "admin"
                admin_password = self.hash_password("admin123@")
                self.add_user_to_db(admin_email, admin_name, admin_username, admin_password, role='admin')
            else:
                self.edit_user_role("admin", "admin")
            conn.commit()
            conn.close()
        except psycopg2.Error as e:
            st.error(f"Database error: {e}")
        #
        #     conn.commit()
        #     conn.close()
        # except psycopg2.Error as e:
        #     st.error(f"Database error: {e}")
        # except Exception as e:
        #     st.error(f"An error occurred: {e}")

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def add_user_to_db(self, email, name, username, password, role='user'):
        hashed_pwd = self.hash_password(password)
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (email, name, username, password, role) VALUES (%s, %s, %s, %s, %s)",
                    (email, name, username, hashed_pwd, role))
            conn.commit()
            conn.close()
            return True
        except psycopg2.IntegrityError:
            st.error("Email or Username already exists.")
            return False
        except psycopg2.Error as e:
            st.error(f"Database error: {e}")
            return False

    def unique_email_in_db(self, email):
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
            result = cursor.fetchone()
            conn.close()
            return result is None
        except psycopg2.Error as e:
            st.error(f"Database error: {e}")
        return True

    def check_user_in_db(self, username):
        if not non_empty_str_check(username):
            return None
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()
            conn.close()
            return result is None
        except psycopg2.Error as e:
            st.error(f"Database error: {e}")
        return True

    def get_user_role(self, username):
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("SELECT role FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else None
        except psycopg2.Error as e:
            st.error(f"Database error: {e}")

    def verify_user(self, username: str, password: str):
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("SELECT password, role FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()
            conn.close()
            print(password)
            print(result)
            print(self.hash_password(password))
            if result:
                stored_hashed_password, role = result
                if stored_hashed_password == self.hash_password(password):
                    return True, role
            return False, None
        except psycopg2.Error as e:
            st.error(f"Database error: {e}")
            return False, None

    def fetch_all_users_with_passwords(self):
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("SELECT email, name, username, password, role FROM users")
            users = cursor.fetchall()
            conn.close()
            return users
        except psycopg2.Error as e:
            st.error(f"Database error: {e}")
            return []

    def edit_user_role(self, username, role):
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET role = %s WHERE username = %s", (role, username))
            conn.commit()
            conn.close()
            return True
        except psycopg2.Error as e:
            st.error(f"Database error: {e}")
            return False

    def delete_user(self, username):
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE username = %s", (username,))
            conn.commit()
            conn.close()
            return True
        except psycopg2.Error as e:
            st.error(f"Database error: {e}")
            return False

    def update_password(self, username, password):
        hashed_pwd = self.hash_password(password)
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET password = %s WHERE username = %s", (hashed_pwd, username))
            conn.commit()
            conn.close()
            return True
        except psycopg2.Error as e:
            st.error(f"Database error: {e}")
            return False

    def update_email(self, username, email):
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET email = %s WHERE username = %s", (email, username))
            conn.commit()
            conn.close()
            return True
        except psycopg2.Error as e:
            st.error(f"Database error: {e}")
            return False

    def update_name(self, username, name):
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET name = %s WHERE username = %s", (name, username))
            conn.commit()
            conn.close()
            return True
        except psycopg2.Error as e:
            st.error(f"Database error: {e}")
            return False

    def get_user_details(self, username):
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("SELECT email, username, name, role FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()
            conn.close()
            data = {
                "email": result[0],
                "username": result[1],
                "name": result[2],
                "role": result[3]
            }
            return data
        except psycopg2.Error as e:
            st.error(f"Database error: {e}")
            return None

    def get_all_users(self):
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM users")
            users = cursor.fetchall()
            conn.close()
            return [user[0] for user in users]
        except psycopg2.Error as e:
            st.error(f"Database error: {e}")
            return []

