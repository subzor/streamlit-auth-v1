import hashlib
import sqlite3

import streamlit as st

# Function to check if a column exists in a table
def column_exists(cursor, table_name, column_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    return any(column[1] == column_name for column in columns)

# Database initialization with schema update handling
def init_db():
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Check if the users table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        table_exists = cursor.fetchone() is not None

        if not table_exists:
            # Create new table with all columns
            cursor.execute('''CREATE TABLE users (
                            email TEXT UNIQUE,
                            username TEXT PRIMARY KEY,
                            password TEXT NOT NULL,
                            role TEXT DEFAULT 'user')''')
        else:
            # Check if role column exists
            if not column_exists(cursor, 'users', 'role'):
                # Add role column to existing table
                cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")
                conn.commit()

        # Check if admin account exists
        cursor.execute("SELECT username FROM users WHERE username = ?", ("admin",))
        admin_exists = cursor.fetchone()

        # Create admin account if it doesn't exist
        if not admin_exists:
            admin_email = "admin@admin.pl"
            admin_username = "admin"
            admin_password = hash_password("admin123")
            cursor.execute("INSERT INTO users (email, username, password, role) VALUES (?, ?, ?, ?)",
                         (admin_email, admin_username, admin_password, "admin"))
        else:
            # Update existing admin account to ensure it has admin role
            cursor.execute("UPDATE users SET role = ? WHERE username = ?", ("admin", "admin"))

        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to add a user to the database
def add_user_to_db(email, username, password, role='user'):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email, username, password, role) VALUES (?, ?, ?, ?)",
                      (email, username, password, role))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        st.error("Email or Username already exists.")
        return False
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return False

# Function to check if an email exists in the database
def check_email_in_db(email):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM users WHERE email = ?", (email,))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return False

# Function to check if a username exists in the database
def check_user_in_db(username):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return False

# Function to verify a user's credentials
def verify_user(username: str, password: str):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT password, role FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()

        if result:
            stored_hashed_password, role = result
            if stored_hashed_password == hash_password(password):
                return True, role
        return False, None
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return False, None

# Function to fetch all users with hashed passwords
def fetch_all_users_with_passwords():
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT email, username, password, role FROM users")
        users = cursor.fetchall()
        conn.close()
        return users
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return []