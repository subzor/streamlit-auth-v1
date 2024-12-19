import io
import os

import streamlit.components.v1 as components
from PIL import Image

from backend.amazon import AmazonScraper
from backend.models.book import Book
from db.db import Database
from navigation import make_sidebar
import streamlit as st

make_sidebar()

db = Database()
user_name = st.session_state.get("LOGGED_USER")
user_details = db.get_user_details(user_name)

st.write(
    f"""
# 🕵️ Secret Company Stuff

This is a secret page that only logged-in users can see.

Don't tell anyone.

For real.

Your user data: 

"""
)
for s, d in user_details.__dict__.items():
    st.write(f"{s.capitalize()}: {d} ")


st.write("")
st.write("")
st.write("")
st.write("")

isbn = st.text_input("Enter ISBN")

if st.button("Get books"):
    amazon: [Book] = AmazonScraper(isbn).get_books()

    for index, book in enumerate(amazon):
        book.trim_()
        st.image(Image.open(io.BytesIO(book.image.image)), caption="Book cover")
        st.text_input(f"Title{index}", book.title)
        st.text_input(f"Author{index}", book.author)
        st.text_input(f"Name{index}", book.name)
        st.text_input(f"Price{index}", book.price)
        st.text_input(f"Currency{index}", book.currency)
        st.text_input(f"Sale price{index}", book.sale_price)
        st.text_input(f"Description{index}", book.description)
        st.text_input(f"Publisher{index}", book.publisher)
        st.text_input(f"Publish year{index}", book.publish_year)
        st.text_input(f"Pages{index}", book.pages)
        st.text_input(f"Category{index}", book.category)
        st.text_input(f"Binding{index}", book.binding)
        st.write("")






