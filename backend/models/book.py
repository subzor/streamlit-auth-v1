"""Book object"""
import inspect
import io
import json
import os

from PIL import Image

from backend.models.enums import Binding, Category
from backend.models.picture import Picture
from backend.utils.const import Paths


class Book:
    def __init__(
        self,
        isbn: str,
        url: str,
        binding: Binding = None,
        title: str = None,
        author: str = None,
        name: str = None,
        price: str = None,
        currency: str = None,
        sale_price: str = None,
        description: str = None,
        publisher: str = None,
        publish_year: str = None,
        pages: str = None,
        image: Picture = None,
        category: Category | list = None,
    ):
        self.isbn = isbn
        self.url = url
        self.binding = binding
        self.title = title
        self.author = author
        self.name = name
        self.price = price
        self.currency = currency
        self.sale_price = sale_price
        self.description = description
        self.publisher = publisher
        self.publish_year = publish_year
        self.pages = pages
        self.image = image
        self.category = category

    # TODO Add trim string
    def trim_(self):
        for i in inspect.getmembers(self):
            if not inspect.ismethod(i[1]):
                if isinstance(i[1], str):
                    setattr(self, i[0], i[1].strip())

    def to_json(self):
        return json.dumps(self.__dict__)


if __name__ == "__main__":
    book = Book(
        isbn="9781471192449",
        url="https://www.amazon.co.uk/Where-Crawdads-Sing-Delia-Owens/dp/1471192446",
        title=" Where the Crawdads Sing",
        author=" Delia Owens ",
        price="6.99",
        currency="GBP",
        sale_price="£6.99",
        description="Where the Crawdads Sing is at once an exquisite ode to the natural world, a heartbreaking coming-of-age story, and a surprising tale of possible",
        publisher="Little, Brown ",
        publish_year="2018",
        pages="384",
        image=Picture(
            url="https://m.media-amazon.com/images/I/81rsjAM3f8L._SL1500_.jpg", isbn="9781471192449"
        ),
        category=[Category.FICTION, Category.MYSTERY],
    )
    # print(book.to_json())
    book.trim_()
    ss = book.to_json()
    aa = json.loads(ss)
    dd = bytes.fromhex(aa["image"]["url"])
    image = Image.open(io.BytesIO(dd))
    image.save(os.path.join(Paths.IMAGE_FOLDER, f"dupa.jpg"))



