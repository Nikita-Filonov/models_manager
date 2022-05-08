from models_manager.manager.exeptions import NegativeValuesException
from models_manager.manager.field.typing import GenericChoices, GenericCategories
from models_manager.schema.schema_template import SchemaTemplate


class NegativeValuesValidator:

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
        self._category = category
        self._schema_template = schema_template

        self._choices = choices
        self._max_length = max_length
        self._min_length = min_length
        self._max_items = max_items
        self._min_items = min_items
        self._gt = gt
        self._ge = ge
        self._lt = lt
        self._le = le

    def _ensure_max_length(self):
        if self._max_length is None:
            raise NegativeValuesException('Attempt to generate negative max length, but "max_length" is None')

        if not issubclass(self._category, str):
            raise NegativeValuesException(
                f'Attempt to generate negative max length on non String field, {self._category}'
            )

    def _ensure_min_length(self):
        if self._min_length is None:
            raise NegativeValuesException('Attempt to generate negative min length, but "min_length" is None')

        if not issubclass(self._category, str):
            raise NegativeValuesException(
                f'Attempt to generate negative min length on non String field, {self._category}'
            )

    def _ensure_gt(self):
        if self._gt is None:
            raise NegativeValuesException('Attempt to generate negative gt, but "gt" is None')

        if not issubclass(self._category, (int, float)):
            raise NegativeValuesException(
                f'Attempt to generate negative gt on non Integer/Decimal field, {self._category}'
            )

    def _ensure_lt(self):
        if self._lt is None:
            raise NegativeValuesException('Attempt to generate negative lt, but "lt" is None')

        if not issubclass(self._category, (int, float)):
            raise NegativeValuesException(
                f'Attempt to generate negative gt on non Integer/Decimal field, {self._category}'
            )

    def _ensure_ge(self):
        if self._ge is None:
            raise NegativeValuesException('Attempt to generate negative ge, but "ge" is None')

        if not issubclass(self._category, (int, float)):
            raise NegativeValuesException(
                f'Attempt to generate negative ge on non Integer/Decimal field, {self._category}'
            )

    def _ensure_le(self):
        if self._le is None:
            raise NegativeValuesException('Attempt to generate negative le, but "le" is None')

        if not issubclass(self._category, (int, float)):
            raise NegativeValuesException(
                f'Attempt to generate negative le on non Integer/Decimal field, {self._category}'
            )

    def _ensure_choices(self):
        if self._choices is None:
            raise NegativeValuesException('Attempt to generate negative choices, but "choices" is None')
