from typing import Union

from models_manager.manager.query.operators import SupportedOperators
from models_manager.utils import dump_value

MODEL_MOCK = '{model}'
SUPPORTED_VALUES = Union[str, list, tuple, int, float]
TEMPLATES = SupportedOperators.to_list()


def template_to_query(name: str, value: SUPPORTED_VALUES):
    """
    :param name: Template name of the field, for example ``id__in``
    :param value: Value of the field for matching the condition
    :return: Will return part of the SQL query

    Example:
        >>> template_to_query('id__in', (1, 2, 3))
        '"{model}"."id" IN (1, 2, 3)'
        >>> template_to_query('name', 5)
        '"{model}"."name" = 5'
        >>> template_to_query('name__not_in', (1, 2, 3))
        '"{model}"."name" NOT IN (1, 2, 3)'
    """
    template, operator = next(filter(lambda t: name.endswith(t[0]), TEMPLATES), ('', '='))
    name = name.replace(template, '')

    return f'"{MODEL_MOCK}"."{name}" {operator} {dump_value(value)}'


def get_query(model: str, *args, **kwargs) -> str:
    """
    :param model: Normalized name of the model
    :param args: Node Q arguments | MyModel.manager.filter(Q(name__in=(1, 2, 3)))
    :param kwargs: Keyword arguments for query | MyModel.manager.filter(name__in=(1, 2, 3))
    :return:
    """
    # simple query - MyModel.manager.filter(name__in=(1, 2, 3))
    # node query -  MyModel.manager.filter(Q(name__in=(1, 2, 3)))

    # resolving query for passed nodes
    # Every Q object should have .defined_query attribute, but if this attribute is
    # None, then we are getting query of this node by our self .to_query()
    node_query = ' AND '.join([node.defined_query or node.to_query() for node in args])

    # resolving query for simple query
    simple_query = ' AND '.join([template_to_query(key, value) for key, value in kwargs.items()])

    # if user passed simple query and node query
    if simple_query and node_query:
        # then we are joining them with AND operator. And replacing model name mock with real model name
        return f'{simple_query} AND {node_query}'.replace(MODEL_MOCK, model)

    # if only one query was passed, then getting this query. And replacing model name mock with real model name
    return (simple_query or node_query).replace(MODEL_MOCK, model)
