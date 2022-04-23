from typing import Union, Type, Callable, _GenericAlias

SUPPORTED_TYPES = (str, int, float, list, dict, bool)

GenericTypes = Union[str, int, float, list, dict, bool, Callable, None]
GenericCategories = Union[
    Type[str],
    Type[int],
    Type[float],
    Type[list],
    Type[dict],
    Type[bool],
    Type[tuple],
    _GenericAlias
]
GenericChoices = Union[list, tuple]
