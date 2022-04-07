from abc import ABC, abstractmethod

from models_manager.constants import TYPE_NAMES
from models_manager.manager.exeptions import ProviderException
from models_manager.manager.field.typing import GenericCategories
from models_manager.utils import random_number, random_string


class Provider(ABC):
    """
    Base class which implements provider interface for constructing
    negative values based on field context
    """

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def value(self):
        return

    @abstractmethod
    def generic(self):
        return

    @abstractmethod
    def string(self):
        return

    @abstractmethod
    def number(self):
        return

    @abstractmethod
    def boolean(self):
        return

    @abstractmethod
    def array(self):
        return

    @abstractmethod
    def object(self):
        return


class NegativeValuesProvider(Provider):
    """
    Common provider with default methods for getting negative values

    If you want to make custom provider, then you have two choices:

    1. Inherit from ``CommonProvider`` and override method that you need
    2. Inherit from ``Provider`` and implement all methods from scratch
    """

    def __init__(self, null: bool, max_length: int, category: GenericCategories, json: str):
        super().__init__()

        self.json = json
        self.null = null
        self.max_length = max_length
        self.category = category

    def value(self):
        func = getattr(self, TYPE_NAMES[self.category], None)

        if func is None:
            supported = ','.join(TYPE_NAMES.keys())
            raise ProviderException(f'Unable to resolve type {self.category}, choose one of supported {supported}')

        return func()

    def generic(self):
        return None if not self.null else random_string()

    def string(self):
        if self.null and self.max_length is None:
            raise ProviderException(f'Provide "max_length" argument for field "{self.json}"')

        return None if (not self.null) else random_string(self.max_length, self.max_length + 50)

    def number(self):
        if not self.null:
            return

        if self.max_length is not None:
            return random_number(self.max_length, self.max_length + 50)

        return random_string()

    def boolean(self):
        return self.generic()

    def array(self):
        return self.generic()

    def object(self):
        return self.generic()
