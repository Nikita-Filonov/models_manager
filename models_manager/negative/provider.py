from datetime import datetime, date, time
from random import choice
from typing import Callable, List, Type

from models_manager.manager.field.typing import GenericCategories, GenericChoices
from models_manager.negative.validator import NegativeValuesValidator
from models_manager.schema.schema_template import SchemaTemplate
from models_manager.utils import random_string, random_number, random_decimal, random_dict, random_list, \
    random_boolean, random_datetime, random_date, random_time


class NegativeValuesProvider(NegativeValuesValidator):
    MIN_ADD = 1
    MAX_ADD = 20
    VALUES_PROVIDERS = {
        int: random_number,
        float: random_decimal,
        str: random_string,
        list: random_list,
        tuple: random_list,
        dict: random_dict,
        bool: random_boolean,
        datetime: random_datetime,
        date: random_date,
        time: random_time
    }

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
            choices: GenericChoices = None,
    ):
        super().__init__(
            category=category,
            schema_template=schema_template,
            max_length=max_length,
            min_length=min_length,
            max_items=max_items,
            min_items=min_items,
            gt=gt,
            ge=ge,
            lt=lt,
            le=le,
            choices=choices
        )

        self._origin = schema_template.origin
        self._args = schema_template.args
        self._inner = schema_template.inner

    @property
    def _value_provider(self) -> Callable:
        if self._origin == 'union':
            return self._choose_provider(args=self._args, is_positive=True)

        return self.VALUES_PROVIDERS[self._origin]

    @property
    def _negative_value_provider(self):
        if self._origin == 'union':
            return self._choose_provider(args=self._args, is_positive=False)

        return self._choose_provider(args=[self._origin], is_positive=False)

    def max_length(self):
        self._ensure_max_length()
        return self._value_provider(self._max_length + self.MIN_ADD, self._max_length + self.MAX_ADD)

    def min_length(self):
        self._ensure_min_length()
        return self._value_provider(1, self._min_length - self.MIN_ADD)

    def max_items(self):
        return self._value_provider(elements=self._max_items + self.MAX_ADD)

    def min_items(self):
        return self._value_provider(elements=self._min_items - (self.MIN_ADD * 2))

    @classmethod
    def null(cls):
        return None

    def gt(self):
        self._ensure_gt()
        return random_decimal(self._gt - self.MAX_ADD, self._gt)

    def ge(self):
        self._ensure_ge()
        return random_decimal(self._ge - self.MAX_ADD, self._ge - self.MIN_ADD)

    def lt(self):
        self._ensure_lt()
        return random_decimal(self._lt, self._lt + self.MAX_ADD)

    def le(self):
        self._ensure_le()
        return random_decimal(self._le + self.MIN_ADD, self._le + self.MAX_ADD)

    def choices(self):
        self._ensure_choices()
        guess_choice = self._value_provider()

        if guess_choice in self._choices:
            return self.choices()

        return guess_choice

    def category(self):
        return self._negative_value_provider()

    def _choose_provider(self, args: List[Type], is_positive=False) -> Callable:
        if is_positive:
            available_providers = list(filter(lambda arg: arg[0] in args, self.VALUES_PROVIDERS.items()))
        else:
            available_providers = list(filter(lambda arg: arg[0] not in args, self.VALUES_PROVIDERS.items()))

        _, provider = choice(available_providers)
        return provider

    def random(self, **kwargs):
        return self._value_provider(**kwargs)
