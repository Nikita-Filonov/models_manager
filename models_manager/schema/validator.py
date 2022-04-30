from typing import Iterable, Type

from models_manager.manager.exeptions import SchemaException
from models_manager.manager.field.typing import GenericChoices
from models_manager.schema.schema_template import SchemaTemplate


def safe_any(iterable: Iterable):
    return any((item is not None) for item in iterable)


class SchemaValidator:
    UNION = 'union'

    def __init__(
            self,
            schema_template: SchemaTemplate,
            choices: GenericChoices = None,
            max_length: int = None,
            min_length: int = None,
            gt: float = None,
            ge: float = None,
            lt: float = None,
            le: float = None,
            max_items: int = None,
            min_items: int = None,
            pattern: str = None,
            title: str = None,
            description: str = None
    ):
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
        self._pattern = pattern
        self._title = title
        self._description = description

        self._args = self._schema_template.args
        self._inner = self._schema_template.inner
        self._origin = self._schema_template.origin

    def _ensure_not_union(self) -> bool:
        return (self._origin != self.UNION) and (self._origin is not None)

    def _ensure_is_optional(self, *category: Type) -> bool:
        return any(issubclass(arg, (*category,)) for arg in self._args)

    def _validate_for_str(self):
        any_length = safe_any((self._max_length, self._min_length))

        if (not self._ensure_not_union()) and any_length and (not self._ensure_is_optional(str)):
            raise SchemaException(f'Attempt to use "max_length"/"min_length"" on non String field "{self._origin}"')

        if self._ensure_not_union():
            if (not issubclass(self._origin, str)) and any_length:
                raise SchemaException(f'Attempt to use "max_length"/"min_length"" on non String field "{self._origin}"')

    def _validate_for_int_float(self):
        any_gt_lt = safe_any((self._gt, self._ge, self._lt, self._le))

        if (not self._ensure_not_union()) and any_gt_lt and (not self._ensure_is_optional(int, float)):
            raise SchemaException(f'Attempt to use "gt"/"ge"/"lt"/"le" on non Decimal field "{self._origin}"')

        if self._ensure_not_union():
            if (not issubclass(self._origin, (int, float))) and any_gt_lt:
                raise SchemaException(f'Attempt to use "gt"/"ge"/"lt"/"le" on non Decimal field "{self._origin}"')

        if (self._gt is not None) and (self._ge is not None):
            raise SchemaException('Properties "gt" and "ge" can not be used at the same time')

        if (self._lt is not None) and (self._le is not None):
            raise SchemaException('Properties "lt" and "le" can not be used at the same time')

    def _validate_for_common(self):
        if self._choices is not None:
            if not isinstance(self._choices, (list, tuple)):
                raise SchemaException('Choices must be Tuple or an Array with enum of values')

    def _validate_for_list_tuple(self):
        any_items = safe_any((self._min_items, self._max_items))
        if (not self._ensure_not_union()) and any_items and (not self._ensure_is_optional(list, tuple)):
            raise SchemaException(f'Attempt to use "min_items"/"max_items" on non Array/Tuple filed "{self._origin}"')

        if self._ensure_not_union():
            if (not issubclass(self._origin, (tuple, list))) and any_items:
                raise SchemaException(
                    f'Attempt to use "min_items"/"max_items" on non Array/Tuple filed "{self._origin}"')

        if (self._min_items or 0) < (self._max_items or 0):
            raise SchemaException('Attribute "min_items" can not be less than "max_items"')
