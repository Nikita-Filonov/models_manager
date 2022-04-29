from typing import _GenericAlias, Union, Optional  # no qa

from models_manager.schema.schema_template import SchemaTemplate


def resolve_typing(annotation: Optional[_GenericAlias]) -> SchemaTemplate:
    """
    Used to turn a type annotation into a convenient object.
    This object will describe annotation and nesting, types, original types

    :param annotation: Optional any generic alias type. For example
    ``List[str]``, ``Dict[str, int]``, ``Union[int, bool]`` etc.
    :return: Resolved dict with original object, args and inners

    Examples:
       resolve_typing(dict) ->  {'origin': <class 'dict'>, 'args': []}
       resolve_typing(Dict[str, int]) -> {'origin': <class 'dict'>, 'args': [<class 'str'>, <class 'int'>]}
       resolve_typing(List[Dict[str, int]]) -> {
           'origin': <class 'list'>,
           'args': [],
           'inner': {
               'origin': <class 'dict'>,
               'args': [<class 'str'>, <class 'int'>]
           }
       }
       resolve_typing(List[Dict[str, Union[int, str]]]) -> {
           'origin': <class 'list'>,
           'args': [],
           'inner': {
               'origin': <class 'dict'>,
               'args': [<class 'str'>],
               'inner': {
                   'origin': 'union',
                   'args': [<class 'int'>, <class 'str'>]
               }
           }
       }
    """
    template = SchemaTemplate()
    if annotation is None:
        return template

    attributes = annotation.__dict__

    origin = attributes.get('__origin__')

    if origin is None:
        template.origin = annotation
        return template

    template.origin = 'union' if origin == Union else origin

    for attr in attributes['__args__']:
        if isinstance(attr, _GenericAlias):
            template.inner = resolve_typing(attr)
            continue

        template.args = [*template.args, attr]

    return template
