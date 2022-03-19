from abc import ABC, abstractmethod

from models_manager.providers.context import ProviderContext
from models_manager.utils import random_dict, random_string, random_list, random_number


class Provider(ABC):
    """
    Base class which implements provider interface for constructing
    negative values based on field context
    """

    @staticmethod
    @abstractmethod
    def string(context: ProviderContext):
        return

    @staticmethod
    @abstractmethod
    def number(context: ProviderContext):
        return

    @staticmethod
    @abstractmethod
    def boolean(context: ProviderContext):
        return

    @staticmethod
    @abstractmethod
    def array(context: ProviderContext):
        return

    @staticmethod
    @abstractmethod
    def object(context: ProviderContext):
        return


class CommonProvider(Provider):
    """
    Common provider with default methods for getting negative values

    If you want to make custom provider, then you have two choices:

    1. Inherit from ``CommonProvider`` and override method that you need
    2. Inherit from ``Provider`` and implement all methods from scratch
    """

    @staticmethod
    def string(context: ProviderContext):
        return None if not context.null else random_string(context.max_length, context.max_length + 50)

    @staticmethod
    def number(context: ProviderContext):
        if not context.null:
            return

        if context.max_length is not None:
            return random_number(context.max_length, context.max_length + 50)

        return random_string()

    @staticmethod
    def boolean(context: ProviderContext):
        return None if not context.null else random_string()

    @staticmethod
    def array(context: ProviderContext):
        return None if not context.null else random_dict()

    @staticmethod
    def object(context: ProviderContext):
        return None if not context.null else random_list()
