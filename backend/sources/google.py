"""Google books api"""

import json
import os
from collections import namedtuple

import requests
from dotenv import load_dotenv

from backend.models.book import Book
from backend.models.output import State
from backend.utils import helpers

LOGGER = helpers.logger(os.path.basename(__file__))


class GoogleBooksApi:
    """
    Main class for obtaining book info from google books api
    :param isbn: isbn of the book
    """

    load_dotenv()
    URL = os.getenv("GOOGLE_URL")
    TOKEN = os.getenv("GOOGLE_TOKEN")

    def __init__(self, isbn: str) -> None:
        self.isbn = isbn
        self.google_header = "&key=" + self.TOKEN
        self.book_object = {"isbn": self.isbn, "url": self.URL}
        self.mapping_attribute = {
            "title": "title",
            "authors": "author",
            "publisher": "publisher",
            "publishedDate": "publish_year",
            "description": "description",
            "pageCount": "pages",
            "categories": "category",
        }
        self.response_object = {}

    def get_book_info(self) -> Book | str:
        """Get book info from Google Books API"""
        try:
            response = requests.get(self.URL + self.isbn + self.google_header).json()
        except Exception as error:
            LOGGER.error(error)
            return State.CONFIG_ERROR

        if "items" in response:
            items = json.dumps(response["items"][0]["volumeInfo"])
            self.response_object = json.loads(
                items, object_hook=lambda d: namedtuple("X", d.keys())(*d.values())
            )

            for key, value in self.mapping_attribute.items():
                self.book_object[value] = self.get_attribute(key)

            return Book(**self.book_object)

    def get_attribute(self, attribute: str) -> any:
        """Get attribute from book object"""
        if hasattr(self.response_object, attribute):
            return getattr(self.response_object, attribute)


if __name__ == "__main__":
    google = GoogleBooksApi("9781984806734")
    book = google.get_book_info()
    print(book)
