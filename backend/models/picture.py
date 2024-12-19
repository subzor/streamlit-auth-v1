"""Book cover image object"""
import glob
import io
import os
from io import BytesIO
from pathlib import Path
from typing import Optional, Union

import requests
from PIL import Image

import backend.models.output as message
from backend.utils import helpers
from backend.utils.const import Paths

LOGGER = helpers.logger(os.path.basename(__file__))


class Picture(dict):
    """?"""

    def __init__(self, url: str, isbn: str):
        self.url = url
        self.isbn = isbn
        self.image = self.get_image()
        dict.__init__(self, url=self.image.hex(), isbn=self.isbn)
        self.image_size = tuple
        self.image_format = str

        self.get_image_info(self.image)

    def __str__(self):
        return self

    def get_image(self) -> Union[bytes, str]:
        """Download image from URL"""
        try:
            request = requests.get(self.url, stream=True)

            if request.status_code == 200 and request.content:
                return request.content
            else:
                return message.State.IMAGE_ERROR

        # TODO error handling.
        except Exception as exc:
            LOGGER.error(exc)
            print(exc)

    def get_image_info(self, image: bytes):
        """Get information about downloaded image"""
        try:
            image = Image.open(BytesIO(image))

            if image.verify():
                print(message.State.IMAGE_ERROR)
                raise Exception(image.verify())

            self.image_size = image.size or None
            self.image_format = image.format or None

        except TypeError as exc:
            LOGGER.error(exc)
            print(message.State.IMAGE_ERROR)

        # TODO error handling.
        except Exception as exc:
            LOGGER.error(exc)
            print(exc)

    def save_image(self):
        self.__check_directory()
        image = Image.open(io.BytesIO(self.image))
        image.save(os.path.join(Paths.IMAGE_FOLDER, f"{self.isbn}.jpg"))

    @staticmethod
    def __check_directory():
        """Check if directory exists"""
        image_path = Path(Paths.IMAGE_FOLDER)
        image_files = glob.glob(os.path.join(image_path, "*"))
        if image_path.exists() and image_path.is_dir():
            for image in image_files:
                try:
                    Path(image).unlink()
                except OSError as exc:
                    LOGGER.error(exc)

        else:
            Path(image_path).mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    file = Picture("https://m.media-amazon.com/images/I/81m9fP+LIPL._SY466_.jpg" , "9781408855652")
    print(file)
