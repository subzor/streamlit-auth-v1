import os
import re
import secrets

from src.consts import Paths


def check_valid_name(name_sign_up: str) -> bool:
    """
    Checks if the user entered a valid name while creating the account.
    """
    name_regex = (r'^[A-Za-z_][A-Za-z0-9_]*')

    if re.search(name_regex, name_sign_up):
        return True
    return False


def check_valid_email(email_sign_up: str) -> bool:
    """
    Checks if the user entered a valid email while creating the account.
    """
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    if re.fullmatch(regex, email_sign_up):
        return True
    return False


def non_empty_str_check(username_sign_up: str) -> bool:
    """
    Checks for non-empty strings.
    """
    empty_count = 0
    for i in username_sign_up:
        if i == ' ':
            empty_count = empty_count + 1
            if empty_count == len(username_sign_up):
                return False

    if not username_sign_up:
        return False
    return True

def generate_random_passwd() -> str:
    """
    Generates a random password to be sent in email.
    """
    password_length = 10
    return secrets.token_urlsafe(password_length)


def validate_password(password):
    # Use the len() function to get the length of the password string and
    # return False right away if the password length is not sufficient
    if (len(password) < 8):
        return False

        # Variables to keep track of whether or not the password contains a
    # character from each category.
    has_lower = False
    has_upper = False
    has_digit = False
    has_symbol = False

    # A string containing all the valid symbol characters
    symbols = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"

    # The loop body will run for each character in the password, with the
    # variable character set to the next character in the string each time.
    # We set the variables above equal to True when we find a character
    # from the associated category.
    for character in password:

        # islower() returns True if character is a lower case letter, so set
        # has_lower to True if so as we have found a lower case letter
        if character.islower():
            has_lower = True

            # isupper() returns True if character is an upper case letter, so set
        # has_upper to True if so as we have found an upper case letter
        if character.isupper():
            has_upper = True

            # isdigit() returns True if character is a digit, so set has_digit to
        # True if so as we have found a digit
        if character.isdigit():
            has_digit = True

            # Technically the isdigit() function will return True for some unusual
        # characters such as superscript ², if we want to strictly allow only
        # the digit characters 0-9 we could use the in operator like this...
        #
        # if character in "0123456789":
        #    has_digit = True

        # The in operator will return true if the character is found in the
        # symbols string, in which case we have found a valid symbol and we
        # set has_symbol to True to recognize this
        if character in symbols:
            has_symbol = True

            # Return true if the password has a lower case letter AND it has an
    # upper case letter AND so on, and false otherwise
    return has_lower and has_upper and has_digit and has_symbol


def is_secrets_toml_file_exists() -> bool:
    """
    Checks if the secrets.toml file exists in the current directory.
    """
    return os.path.exists(Paths.SECRETS_FILE)





