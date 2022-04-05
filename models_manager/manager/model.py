from functools import reduce
from typing import Union

from models_manager.manager.manager import ModelManager


class Meta(type):
    def __new__(mcs, name, bases, attrs):
        safe_name = mcs.resolve_name(name, attrs)
        safe_attrs = mcs.resolve_attrs(bases, attrs)

        cls = type.__new__(mcs, name, bases, attrs)
        cls.manager = ModelManager(safe_name, bases, **safe_attrs)

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


class Model(metaclass=Meta):
    database = None
    identity = 'id'
    extended_by = None
