from random import randint, choice
from string import ascii_letters, digits

from faker import Faker

fake = Faker()


def random_string(start: int = 20, end: int = 50) -> str:
    """
    :param start:
    :param end:
    :return:
    """
    return ''.join(choice(ascii_letters + digits) for _ in range(randint(start, end)))


def random_number(start: int = 5, end: int = 50) -> int:
    return randint(start, end)


def random_dict(keys_count=5, types=(str, int, bool), **kwargs) -> dict:
    """
    :param keys_count: max number of keys that's will be in dictionary
    :param types: types that's will be in dictionary
    :param kwargs: additional settings which ``pydict`` takes
    :return: random dictionary
    """
    return fake.pydict(nb_elements=keys_count, value_types=types, **kwargs)


def random_list(elements=5, types=(str, int, bool), **kwargs):
    """
    :param elements: max number of elements that's will be in list
    :param types: types that's will be in list
    :param kwargs: additional settings which ``pylist`` takes
    :return: random list
    """
    return fake.pylist(nb_elements=elements, value_types=types, **kwargs)
