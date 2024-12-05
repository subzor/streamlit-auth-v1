from backend.sources.amazon import AmazonScraper
from db.db import Database
from navigation import make_sidebar
import streamlit as st

make_sidebar()

db = Database()
user_name = st.session_state.get("LOGGED_USER")
user_data = db.get_user_details(user_name)

st.write(
    f"""
# 🕵️ Secret Company Stuff

Your user data: 

"""
)
for s, d in user_data.items():
    st.write(f"{s.capitalize()}: {d} ")

isbn = st.text_input("Enter ISBN")

if isbn and isbn.isdigit() and len(isbn) >= 13:
    if st.button("Get Book"):
        ss = AmazonScraper(isbn).get_books()

        st.write(ss[0].isbn)
        st.write(ss[0].url)
        st.write(ss[0].binding.value)
        st.write(ss[0].title)
        st.write(ss[0].author)
        st.write(ss[0].name)
        st.write(ss[0].price)
        st.write(ss[0].currency)
        st.write(ss[0].sale_price)
        st.write(ss[0].description)
        st.write(ss[0].publisher)
        st.write(ss[0].publish_year)
        st.write(ss[0].pages)
        st.image(ss[0].image.image)
        st.write(ss[0].category if isinstance(ss[0].category, list) else ss[0].category.value)



