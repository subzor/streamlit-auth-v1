"""Amazon scraper"""

import os
from threading import Lock

import chromedriver_autoinstaller
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.webdriver import WebDriver

from backend.models.book import Book
from backend.models.enums import Binding
from backend.models.picture import Picture
from backend.utils.helpers import logger
from backend.utils.helpers import get_binding_from_string
from backend.utils.helpers import get_contain_element
from backend.utils.helpers import get_locator
from backend.utils.helpers import run_jobs
from selenium import webdriver
from selenium.webdriver import ChromeOptions


LOGGER = logger(os.path.basename(__file__))


class AmazonConfig:
    """Config for Amazon scraper"""

    def __init__(self) -> None:
        self.amazon_urls = ["https://amazon.com"]

    @staticmethod
    def build_amazon_url(url: str, isbn: str) -> str:
        """Return url for Amazon search"""
        return f"{url}/s?k={isbn}"


class AmazonWebDriver:
    """Web driver for Amazon"""
    HEADERS = 'User-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"'

    def __init__(self) -> None:
        chromedriver_autoinstaller.install()
        self.options = ChromeOptions()
        self.options.add_argument(self.HEADERS)
        self.options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=self.options)

    def get_driver(self) -> WebDriver:
        """Get driver"""
        return self.driver


class AmazonLocators:
    """Locators for Amazon sites"""

    SEARCH_LINKS = get_locator("a", "class", get_contain_element("a-link-normal"))
    PRODUCT_DETAILS = get_locator("div", "id", "detailBullets_feature_div")
    PRODUCT_DETAIL_ITEMS = get_locator("span", "class", "a-list-item")
    PRODUCT_ISBN_DIV = get_locator(
        "div", "id", get_contain_element("book_details-isbn13")
    )
    PRODUCT_ISBN = get_locator(
        "div", "class", get_contain_element("rpi-attribute-value")
    )
    PRODUCT_TITLE = get_locator("span", "id", "productTitle")
    PRODUCT_DESCRIPTION = get_locator("div", "id", "bookDescription_feature_div")
    PRODUCT_CATEGORY = get_locator("ul", "class", get_contain_element("zg_hrsr"))
    PRODUCT_AUTHOR_DIV = get_locator("div", "id", get_contain_element("bylineInfo"))
    PRODUCT_AUTHOR = get_locator("span", "class", get_contain_element("author notFaded"))
    PRODUCT_PRICE = get_locator("span", "id", "price")
    PRODUCT_OPTIONAL_PRICE = get_locator("div", "id", "corePrice_feature_div")
    PRODUCT_IMAGE = get_locator("img", "data-a-image-name", "landingImage")


class AmazonScraper:
    """
    Main class for obtaining information from amazon sites
    :param isbn: isbn of the book
    """

    def __init__(self, isbn: str) -> None:
        self.amazon_config = AmazonConfig()
        self.lock = Lock()
        self.driver = AmazonWebDriver().get_driver()
        self.isbn = isbn
        self.url_search_list = run_jobs(
            self.amazon_config.amazon_urls, self.__get_url_from_search_sites
        )

    def __get_url_from_search_sites(self, url: str) -> list:
        """Return list of urls"""
        url_list = list()

        try:
            page = self.get_page_source(AmazonConfig.build_amazon_url(url, self.isbn))
            soup = BeautifulSoup(page, "lxml")
        except ConnectionError as exc:
            LOGGER.warning(exc)
            return url_list

        try:
            links = soup.findAll(*AmazonLocators.SEARCH_LINKS)
        except AttributeError as exc:
            LOGGER.error(exc)
            return url_list
        if links:
            for link in links:
                if self.isbn in link.attrs["href"] and (
                    "Hardcover" in link.get_text() or "Paperback" in link.get_text()
                ):
                    url_list.append(url + link.attrs["href"])

        return url_list

    def get_page_source(self, url):
        ''' Get page source '''
        self.lock.acquire()
        self.driver.get(url)
        sources = self.driver.page_source
        self.lock.release()
        return sources

    def get_books(self) -> list[Book]:
        """Return list of books"""
        return run_jobs(self.url_search_list, self.get_product)

    def get_product(self, url: str) -> list[Book]:
        """Return list of book object"""
        page = self.get_page_source(url)
        try:
            soup = BeautifulSoup(page, "lxml", from_encoding=page)
        except ConnectionError as exc:
            LOGGER.warning(exc)
            return []

        isbn = self._get_isbn(soup)
        if not isbn == self.isbn:
            return []

        author = self._get_author(soup)
        title = self._get_title(soup)

        if title and author:
            name = f"{title} - {author}"
        else:
            name = ""

        price, currency = self._get_price_and_currency(soup)
        description = self._get_description(soup)
        details = self._get_book_details(soup)

        if details:
            publish_details, bind_details = self._get_publish_and_binding_details(
                details
            )
        else:
            publish_details, bind_details = "", ""

        if publish_details:
            publisher = self._get_publisher(publish_details)
            year = self._get_year(publish_details)
        else:
            publisher, year = "", ""

        if bind_details:
            binding, pages = self._get_binding_and_number_of_pages(bind_details)
        else:
            binding, pages = "", ""

        image = Picture(self._get_image(soup), self.isbn)
        category = self._get_category_list(soup)

        return [
            Book(
                isbn=isbn,
                url=url,
                binding=binding,
                title=title,
                author=author,
                name=name,
                price=price,
                currency=currency,
                description=description,
                publisher=publisher,
                publish_year=year,
                pages=pages,
                image=image,
                category=category,
            )
        ]

    def _get_publisher(self, publish_details: str) -> str:
        """Return publisher"""
        try:
            publisher = publish_details.split(":")[1]
            publisher = publisher.split(";")[0].replace("\n", "").split("(")[0]
        except Exception as exc:
            LOGGER.info(exc)
            return ""
        return self._encode_string(publisher)

    def _get_binding_and_number_of_pages(self, bind_info: str) -> tuple[Binding, str]:
        """Return binding"""
        try:
            binding, pages = bind_info.split(":")
            binding = binding.replace("\n", "")
            pages = self._encode_string(pages).split(" ")[0]
        except Exception as exc:
            LOGGER.info(exc)
            return Binding.OTHER, ""
        bind = self._encode_string(binding)
        return get_binding_from_string(bind), pages

    def _get_price_and_currency_from_string(self, price_string: str) -> tuple[str, str]:
        """Return price and currency from string"""
        if (gbp_curr := "\xA3") in price_string:
            price = price_string.split(gbp_curr)
            price = self._remove_blank_element_and_get_first(price)
            currency = "GBP"

        elif (usd_curr := "\u0024") in price_string:
            price = price_string.split(usd_curr)
            price = self._remove_blank_element_and_get_first(price)
            currency = "USD"
        else:
            currency = ""
            price = price_string

        return price, currency

    def _get_optional_price_and_currency(self, soup: BeautifulSoup) -> tuple[str, str]:
        """Return optional price and currency"""
        try:
            price_string = soup.find(*AmazonLocators.PRODUCT_OPTIONAL_PRICE).get_text()
            price_string = price_string.replace("\n", "").strip()
            if price_string:
                price, currency = self._get_price_and_currency_from_string(price_string)
            else:
                price, currency = "", ""
        except Exception as exc:
            LOGGER.info(exc)
            return "", ""

        return price, currency

    def _get_price_and_currency(self, soup: BeautifulSoup) -> tuple[str, str]:
        """Return price and currency"""
        try:
            price_string = soup.find(*AmazonLocators.PRODUCT_PRICE).get_text()
            if price_string:
                price, currency = self._get_price_and_currency_from_string(price_string)
            else:
                price, currency = self._get_optional_price_and_currency(soup)
        except Exception as exc:
            LOGGER.info(exc)
            price, currency = self._get_optional_price_and_currency(soup)

        return price, currency

    @staticmethod
    def _get_isbn(soup: BeautifulSoup) -> str:
        """Return isbn"""
        try:
            isbn = (
                soup.find(*AmazonLocators.PRODUCT_ISBN_DIV)
                .find(*AmazonLocators.PRODUCT_ISBN)
                .findNext("span")
                .get_text(strip=True)
                .replace("-", "")
            )
        except AttributeError as exc:
            LOGGER.info(exc)
            return ""

        return isbn

    @staticmethod
    def _get_title(soup: BeautifulSoup) -> str:
        """Return title"""
        try:
            author = soup.find(*AmazonLocators.PRODUCT_TITLE).get_text()
        except AttributeError as exc:
            LOGGER.info(exc)
            return ""
        return author

    @staticmethod
    def _get_author(soup: BeautifulSoup) -> str:
        """Return author"""
        try:
            author = soup.find(*AmazonLocators.PRODUCT_AUTHOR).findNext("a").get_text()
        except AttributeError as exc:
            LOGGER.info(exc)
            return ""

        return author

    @staticmethod
    def _remove_blank_element_and_get_first(price_string: list[str]) -> str:
        """Remove blank element and get first element from list"""
        if "" in price_string:
            price_string.remove("")
        return price_string[0]

    @staticmethod
    def _get_description(soup: BeautifulSoup) -> str:
        """Return description"""
        try:
            description = soup.find(*AmazonLocators.PRODUCT_DESCRIPTION).get_text()
            description = description.rstrip("Read more")
        except AttributeError as exc:
            LOGGER.info(exc)
            return ""
        return description

    # TODO Add convert image to base64/other format
    @staticmethod
    def _get_image(soup: BeautifulSoup) -> str:
        """Return image"""
        try:
            image = soup.find(*AmazonLocators.PRODUCT_IMAGE).get("src")
        except AttributeError as exc:
            LOGGER.info(exc)
            return ""
        return image

    @staticmethod
    def _get_year(publish_details: str) -> str:
        """Return year"""
        try:
            year = publish_details.replace(")", "").replace("\n", "").strip()
            year = year[-4:]
        except AttributeError as exc:
            LOGGER.info(exc)
            return ""
        return year

    @staticmethod
    def _get_category_list(soup: BeautifulSoup) -> list:
        """Return category list"""
        try:
            categories = (
                soup.find(*AmazonLocators.PRODUCT_DETAILS)
                .find(*AmazonLocators.PRODUCT_CATEGORY)
                .find_all(name="span")
            )
        except AttributeError as exc:
            LOGGER.error(exc)
            return []

        categories_list = []
        for category in categories:
            cat = category.get_text()
            cat = cat.split("in", 1)[1].split("(")[0]
            categories_list.append(cat)

        return categories_list

    @staticmethod
    def _get_book_details(soup: BeautifulSoup) -> list | None:
        """Return book details"""
        try:
            details = soup.find(*AmazonLocators.PRODUCT_DETAILS).findAll(
                *AmazonLocators.PRODUCT_DETAIL_ITEMS
            )
        except AttributeError as exc:
            LOGGER.info(exc)
            return None
        return details

    @staticmethod
    def _get_publish_and_binding_details(details: list) -> tuple[str, str]:
        """Return publish and binding details"""
        publish_details = ""
        bind_info = ""
        for detail in details:
            if "Publisher" in detail.get_text():
                publish_details = detail.get_text()
            if "Hardcover" in detail.get_text() or "Paperback" in detail.get_text():
                bind_info = detail.get_text()

        return publish_details, bind_info

    @staticmethod
    def _encode_string(text: str) -> str:
        """Return encoded string"""
        return text.encode("ascii", "ignore").decode("utf-8").strip().rstrip()


if __name__ == "__main__":
    ss = AmazonScraper("9781471192449").get_books()
    print(ss)