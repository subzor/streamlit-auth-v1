import logging
import os
import re
from queue import Queue
from re import Pattern
from threading import Thread
from typing import Callable

from backend.models.enums import Binding

# TODO move to db.
# import settings

os.environ["SETTINGS_MODULE"] = "settings-temp"


def logger(source: str) -> logging.Logger:
    logging_path = os.path.expanduser("~\\book.log")
    logging.basicConfig(
        filename=logging_path,
        level=logging.WARN,
        format="%(asctime)s %(name)s %(message)s",
    )
    return logging.getLogger(source)


def get_locator(
        marker: str, by: str, value: str | Pattern
) -> tuple[str, dict[str, str]]:
    """Return locator for beautifulsoup"""
    return marker, {by: value}


def get_contain_element(element: str) -> Pattern:
    """Return pattern for contain element"""
    return re.compile(f".*{element}.*")


def get_binding_from_string(bind: str) -> Binding:
    """Return binding object from string"""

    if "paperback" in bind.lower():
        return Binding.PAPERBACK
    elif "hardcover" in bind.lower():
        return Binding.HARDCOVER
    elif "hard with" in bind.lower():
        return Binding.HARDCOVER_WITH
    elif "mass market paperback" in bind.lower():
        return Binding.MASS_MARKET_PAPERBACK
    else:
        return Binding.OTHER


def run_jobs(parameters: list, method_name: Callable) -> list:
    """Job runner - Spawn threads and run jobs depending on number of parameters
    :param parameters: list of parameters, if type of parameter is tuple then it will be unpacked to method as single parameter
    :param method_name: method to run
    :return: list of results: list of results from methods in method_name

    Remember to return list in called method !!
    """

    job = Queue()
    threads_list = list()
    job_result = list()

    for param in parameters:
        if type(param) is tuple:
            thread = Thread(
                target=lambda queue, *args: queue.put(method_name(*args)),
                args=(job, *param),
            )
        else:
            thread = Thread(
                target=lambda queue, *args: queue.put(method_name(*args)),
                args=(job, param),
            )
        thread.start()
        threads_list.append(thread)

    # Join all the threads
    for thread in threads_list:
        thread.join()
        job_result.extend(job.get())

    return job_result


# TODO move to db.
# def get_user_agent() -> dict:
#     """Return random user agent for header"""
#     return random.choice(settings.user_agent)
