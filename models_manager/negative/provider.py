from typing import Callable

from models_manager.manager.field.typing import GenericCategories
from models_manager.schema.schema_template import SchemaTemplate
from models_manager.utils import random_string, random_number, random_decimal, random_dict, random_list


class NegativeValuesProvider1:
    MIN_ADD = 1
    MAX_ADD = 20

    def __init__(
            self,
            category: GenericCategories,
            schema_template: SchemaTemplate,
            max_length: int = None,
            min_length: int = None,
            max_items: int = None,
            min_items: int = None,
            gt: float = None,
            ge: float = None,
            lt: float = None,
            le: float = None,
    ):
        self._category = category
        self._max_length = max_length
        self._min_length = min_length

        self._gt = gt
        self._ge = ge
        self._lt = lt
        self._le = le

        self._origin = schema_template.origin
        self._args = schema_template.args

    @property
    def _value_provider(self) -> Callable:
        if issubclass(self._origin, str):
            return random_string

        if issubclass(self._origin, int):
            return random_number

        if issubclass(self._origin, float):
            return random_decimal

    def max_length(self):
        return self._value_provider(self._max_length + self.MIN_ADD, self._max_length + self.MAX_ADD)

    def min_length(self):
        return self._value_provider(self._min_length - self.MAX_ADD, self._min_length - self.MIN_ADD)

    @classmethod
    def null(cls):
        return None

    def gt(self):
        return random_decimal(self._gt - self.MAX_ADD, self._gt)

    def ge(self):
        return random_decimal(self._ge - self.MAX_ADD, self._ge - self.MIN_ADD)

    def lt(self):
        return random_decimal(self._lt, self._lt + self.MAX_ADD)

    def le(self):
        return random_decimal(self._le + self.MIN_ADD, self._le + self.MAX_ADD)

    def choices(self):
        return

    def category(self):
        if self._origin == 'union':
            raise NotImplementedError('TODO')

        if issubclass(self._origin, str):
            return random_number()

        if issubclass(self._origin, int):
            return random_string()

        if issubclass(self._origin, float):
            return random_string()

        if issubclass(self._origin, (list, tuple)):
            return random_dict()

        if issubclass(self._origin, dict):
            return random_list()

        if issubclass(self._origin, bool):
            return random_number()
