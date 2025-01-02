import os

from frontend.widgets import SecretsPage
from navigation import make_sidebar
import streamlit as st

make_sidebar()

st.title(f"""
# 🏥 Secrets
""")

secrets_forms = SecretsPage()

if st.checkbox("Show secrets"):
    secrets_forms.secrets_widget()


