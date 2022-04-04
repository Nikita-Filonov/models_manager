from enum import Enum

from models_manager.constants import TYPE_NAMES
from models_manager.manager.field.typing import GenericCategories, GenericTypes


def get_enum_value(category: GenericCategories, default: GenericTypes):
    return category.get_value(default) if hasattr(category, 'get_value') else default.value


class SchemaProvider:
    def __init__(self, category, is_related, is_nullable, max_length, default):
        self._category = category
        self.is_related = is_related
        self.is_nullable = is_nullable
        self.max_length = max_length
        self.default = default

    @property
    def safe_category(self):
        if issubclass(self._category, Enum):
            return type(get_enum_value(self._category, self.default))

        return self._category

    @property
    def category_name(self):
        if self._category in TYPE_NAMES.keys():
            return TYPE_NAMES[self._category]

        if issubclass(self._category, Enum):
            return 'enum'

        return TYPE_NAMES[str]

    def schema(self):
        func = getattr(self, self.category_name, None)

        if callable(func):
            return func()

        return self.generic()

    def generic(self):
        field_type = TYPE_NAMES[self.safe_category]
        field_type_safe_null = [field_type, 'null'] if (self.is_nullable or self.is_related) else field_type
        return {"type": field_type_safe_null}

    def string(self):
        template = self.generic()

        if self.max_length is not None:
            template = {**template, 'minLength': 0, 'maxLength': self.max_length}

        return template

    def enum(self):
        template = self.generic()
        enum_values = [get_enum_value(self._category, enum) for enum in self._category]
        return {**template, 'enum': enum_values}
