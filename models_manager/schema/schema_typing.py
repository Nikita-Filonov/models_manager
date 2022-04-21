from typing import _GenericAlias, Union, Dict, Optional  # no qa

ORIGIN = 'origin'
ARGS = 'args'
INNER = 'inner'


def resolve_typing(annotation: Optional[_GenericAlias]) -> Dict[str, Union[None, list, str]]:
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
    template = {ORIGIN: None, ARGS: []}
    if annotation is None:
        return template

    attributes = annotation.__dict__

    origin = attributes.get('__origin__')

    if origin is None:
        return {**template, ORIGIN: annotation}

    template[ORIGIN] = 'union' if origin == Union else origin

    for attr in attributes['__args__']:
        if isinstance(attr, _GenericAlias):
            template[INNER] = resolve_typing(attr)
            continue

        template[ARGS] = [*template[ARGS], attr]

    return template
