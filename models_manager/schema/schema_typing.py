from typing import _GenericAlias, Union, Dict, Optional

ORIGIN = 'origin'
ARGS = 'args'
INNER = 'inner'


def resolve_typing(annotation: _GenericAlias) -> Dict[str, Union[None, list, str]]:
    """
    :param annotation:
    :return:
    """
    attributes = annotation.__dict__
    template = {ORIGIN: None, ARGS: []}

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


print(resolve_typing(Optional[str]))
