from random import choice, randint
from string import ascii_letters

from app.config.constants import HTTP_METHODS_LIST


def get_random_ascii_letters_string(length: int = 10) -> str:
    return "".join(choice(ascii_letters) for _ in range(length))


def get_random_http_method() -> str:
    return choice(HTTP_METHODS_LIST)


def get_random_path(max_nr_parts: int = 4, max_part_length: int = 10) -> str:
    nr_parts = randint(1, max_nr_parts)

    path = ""
    for _ in range(nr_parts):
        part_length = randint(1, max_part_length)
        part = get_random_ascii_letters_string(part_length)
        path = f"{path}/{part}"

    return path
