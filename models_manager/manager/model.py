from copy import deepcopy
from functools import reduce
from typing import Union, Dict, List, Any

from models_manager.manager.field.field import Field
from models_manager.manager.managers.mixin import ManagerMixin


class Meta(type):
    CONFIG = 'Config'

    def __new__(mcs, name, bases, attrs):
        safe_name = mcs.resolve_name(name, attrs)
        safe_attrs = mcs.resolve_attrs(bases, attrs)

        safe_attrs = mcs.resolve_config(safe_attrs, attrs.get(mcs.CONFIG))

        cls = type.__new__(mcs, name, bases, attrs)
        cls.manager = ManagerMixin(safe_name, bases, **safe_attrs)

        return cls

    @classmethod
    def resolve_attrs(mcs, bases: tuple, attrs: dict) -> dict:
        """
        :param bases: Tuple of mro class bases including super class
        :param attrs: All model attributes
        :return: All model attributes + override attributes from parent classes
        """
        # if modes is inherited
        if len(bases) > 0:
            # resolving mro tree and excluding object
            inherit_mro = list(filter(lambda cls: (cls is not object), bases[0].mro()))

            # if len of inherit_mro equal to 1 or less, we do not need to reduce attributes
            if len(inherit_mro) <= 1:
                return attrs

            # reversing mro list and removing first element
            reversed_inherit_mro = list(reversed(inherit_mro))
            reversed_inherit_mro.pop(0)  # for model first element is always Model class

            # reducing attributes from reversed_inherit_mro, with initial attrs
            return reduce(lambda a, b: {**b.__dict__, **a}, reversed_inherit_mro, attrs)

        # if model is not inherited thn just return it self attributes
        return attrs

    @classmethod
    def resolve_name(mcs, name: str, attrs: dict) -> str:
        """
        :param name: Name of the model
        :param attrs: All model attributes
        :return: Will return models name as string

        Checks if model is extended by other model and if yes, then
        we should use ``extended_by`` model name for queries
        """
        extended_by: Union[Meta, None] = attrs.get('extended_by')
        return extended_by.__name__ if extended_by else name

    @classmethod
    def resolve_config(mcs, attrs: dict, config=None) -> Dict[str, Any]:
        if config is None:
            return attrs

        return {key: value for key, value in attrs.items() if (key not in config.exclude_fields)}


class Model(metaclass=Meta):
    database = None
    identity = 'id'
    extended_by = None

    def __init__(
            self,
            exclude_schema: List[Union[Field, str]] = None,
            exclude_dict: List[Union[Field, str]] = None,
            ignore_validation=False,
            **kwargs
    ):
        self.manager: ManagerMixin = deepcopy(self.manager)
        self.manager.apply_values(**kwargs)
        self.manager.exclude_schema = exclude_schema
        self.manager.exclude_dict = exclude_dict
        self.manager.ignore_validation = ignore_validation

        fields: Dict[str, Field] = self.manager.fields(json_key=False)
        self.__apply_to_fields(fields)

    def __apply_to_fields(self, field: Dict[str, Field]):
        for field_name, field in field.items():
            setattr(self, field_name, field)

    def __str__(self):
        return f'<Model: {self.__class__.__name__}>'
