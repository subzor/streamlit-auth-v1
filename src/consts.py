from os import path
from pathlib import Path


ROOT_PATH = Path(path.dirname(path.abspath(__file__))).parent


class Paths:
    SRC_DIR = path.join(ROOT_PATH, "src")
    STREAMLIT_DIR = path.join(ROOT_PATH, ".streamlit")
    SECRETS_FILE = path.join(STREAMLIT_DIR, "secrets.toml")
    CONFIG_FILE = path.join(STREAMLIT_DIR, "config.toml")
