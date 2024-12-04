

from frontend.forms import SettingsForms
from navigation import make_sidebar
import streamlit as st

make_sidebar()

st.write(f"""
# 🔓 Settings
""")
st.write("Personal data can be changed here")


settings_forms = SettingsForms()


settings_forms.change_password_form()
settings_forms.change_name_form()
settings_forms.change_email_form()


