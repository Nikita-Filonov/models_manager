from typing import Union, Type, Callable

from models_manager.manager.abs_model import AbsModel

SUPPORTED_TYPES = (str, int, float, list, dict, bool, AbsModel)

GenericTypes = Union[str, int, float, list, dict, bool, AbsModel, Callable, None]
GenericCategories = Union[
    Type[str],
    Type[int],
    Type[float],
    Type[list],
    Type[dict],
    Type[bool],
    Type[AbsModel]
]
GenericChoices = Union[list, tuple]
