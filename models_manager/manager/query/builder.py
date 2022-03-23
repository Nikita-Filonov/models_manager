from typing import Union

from models_manager.manager.query.operators import SupportedOperators
from models_manager.utils import dump_value

MODEL_MOCK = '{model}'
SUPPORTED_VALUES = Union[str, list, tuple, int, float]


def template_to_query(name: str, value: SUPPORTED_VALUES):
    templates = SupportedOperators.to_list()
    template, operator = next(filter(lambda t: name.endswith(t[0]), templates), ('', '='))

    name = name.replace(template, '')

    return f'"{MODEL_MOCK}"."{name}" {operator} {dump_value(value)}'


def get_query(model: str, *args, **kwargs) -> str:
    node_query = ''
    if args:
        node_query = ''.join([node.defined_query or node.to_query() for node in args])

    simple_query = ' AND '.join([template_to_query(key, value) for key, value in kwargs.items()])

    if simple_query and node_query:
        return f'{simple_query} AND {node_query}'.replace(MODEL_MOCK, model)

    return (simple_query or node_query).replace(MODEL_MOCK, model)
