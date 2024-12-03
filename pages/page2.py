import pandas as pd

from db.db import fetch_all_users_with_passwords
from navigation import make_sidebar
import streamlit as st

make_sidebar()

st.write(f'Welcome to the {st.session_state.get("ROLE")} page!')
if st.session_state.get('ROLE') == 'admin':
    st.title("User Data")
    user_data = fetch_all_users_with_passwords()
    df = pd.DataFrame(user_data, columns=["Email", "Name", "Username", "Password", "Role"])
    st.dataframe(df)

else:
    st.write("You do not have permission to view data from this page.")