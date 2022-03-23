import functools
import logging
import re
from random import choice, randint
from string import ascii_letters, digits
from time import sleep

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


def retry(times, exceptions, delay=2):
    """
    Retry Decorator
    Retries the wrapped function/method `times` times if the exceptions listed
    in ``exceptions`` are thrown
    :param delay:
    :param times: The number of times to repeat the wrapped function/method
    :type times: Int
    :param exceptions: List or tuple of exceptions that trigger a retry attempt
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < times:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    logging.warning(
                        'Exception thrown when attempting to run %s, attempt '
                        '%d of %d' % (func, attempt, times)
                    )
                    attempt += 1
                sleep(delay)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def serializer(cursor, many=False):
    """
    :param many:
    :param cursor:
    :return:

    Will convert db row to dict.

    For example table with columns like
    | id | name | email |
    | 1 | some_name | some_email@mail.com |
    will return row: (1, 'some_name', 'some_email@mail.com').
    After serializing such row, result would be like:
    {'id': 1, 'name': 'some_name', 'email': 'some_email@mail.com'}.
    """
    columns = [column[0] for column in cursor.description]
    result = [dict(zip(columns, row)) for row in cursor.fetchall()]
    if many:
        return result

    if len(result) == 0:
        return

    return result[0]


def binding(values) -> str:
    """
    Method makes bind string for db values.

    Example:
    some_values = [1, 2, 3, 4, 5]
    binding(some_values) -> '%s, %s, %s, %s, %s'
    """
    return ', '.join(['%s' for _ in range(len(values))])


def dump_fields(fields) -> str:
    """
    Method that helps to wrap columns in double quotes.

    Example:
    some_fields = ['id', 'title', 'subtitle']
    dump_fields(some_fields) -> '"id", "title", "subtitle"'
    """
    return f', '.join([f'"{field}"' for field in fields])


def dump_value(value):
    """
    :param value:
    :return:
    """
    if isinstance(value, bool):
        return 'true' if value else 'false'

    if isinstance(value, str):
        return f"'{value}'"

    if value is None:
        return "null"

    return value


def normalize_model(model) -> str:
    """
    Model normalizer. Makes model name from "CamelCase"
    to "snake_case" convention.

    Example:
    class MyModel(Model):
       id: int = Field(default=1)
       last_name: str = Field(default='some_last_name')
       username: str = Field(default='some', only_json=True)

    self.__normalized_model -> 'my_model'
    """
    model_parts = re.findall('[A-Z][^A-Z]*', model)
    return '_'.join([part.lower() for part in model_parts])


def where(model, operand='AND', operator='=', start='WHERE', **kwargs) -> str:
    """
    :param start: WHERE, AND, OR
    :param model: Name of database table
    :param operand: Logic operand like 'AND', 'OR' etc.
    :param operator: Operator like '=', '<', '>' etc.
    :param kwargs:
    :return:

    Will return formatted where query
    """
    bind = f' {operand} '.join([f'"{model}"."{field}" {operator} %s' for field in kwargs])
    return f' {start} {bind};'
