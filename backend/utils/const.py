from os import path
from pathlib import Path

ROOT_PATH = Path(path.dirname(path.abspath(__file__))).parent.parent


class Paths:
    ROOT_PATH = ROOT_PATH
    TESTS = path.join(ROOT_PATH, "tests")
    RESOURCES = path.join(ROOT_PATH, "resources")
    IMAGE_FOLDER = path.join(RESOURCES, "images")