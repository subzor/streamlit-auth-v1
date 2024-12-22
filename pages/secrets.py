import os

from frontend.widgets import SecretsPage
from navigation import make_sidebar
import streamlit as st

make_sidebar()

st.title(f"""
# 🏥 Secrets
""")

secrets_forms = SecretsPage()

print(os.getenv("POSTGRESQL_DBNAME"))
print(os.getenv("POSTGRESQL_USER"))
print(os.getenv("POSTGRESQL_PASSWORD"))
print(os.getenv("POSTGRESQL_HOST"))
print(os.getenv("POSTGRESQL_PORT"))

if st.checkbox("Show secrets"):
    secrets_forms.secrets_widget()


