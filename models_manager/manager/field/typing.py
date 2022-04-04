from enum import Enum
from typing import Union, Type, Callable

SUPPORTED_TYPES = (str, int, float, list, dict, bool, Enum)

GenericTypes = Union[str, int, float, list, dict, bool, Enum, Callable, None]
GenericCategories = Union[Type[str], Type[int], Type[float], Type[list], Type[dict], Type[bool], Type[Enum]]
