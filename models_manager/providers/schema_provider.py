from models_manager.constants import TYPE_NAMES
from models_manager.manager.abs_model import AbsModel
from models_manager.manager.field.typing import GenericCategories, GenericTypes, GenericChoices


class SchemaProvider:
    def __init__(self, category: GenericCategories,
                 default: GenericTypes,
                 choices: GenericChoices,
                 is_related: bool,
                 is_nullable: bool,
                 max_length: int):
        self._category = category
        self.is_related = is_related
        self.is_nullable = is_nullable
        self.max_length = max_length
        self.default = default
        self.choices = choices

    @property
    def safe_category(self):
        if issubclass(self._category, AbsModel):
            # TODO handle List[Model]
            return dict

        return self._category

    @property
    def category_name(self):
        if self._category in TYPE_NAMES.keys():
            return TYPE_NAMES[self._category]

        if issubclass(self._category, AbsModel):
            return 'model'

        return TYPE_NAMES[str]

    def schema(self):
        func = getattr(self, self.category_name, None)

        if callable(func):
            return func()

        return self.generic()

    def generic(self):
        field_type = TYPE_NAMES[self.safe_category]
        field_type_safe_null = [field_type, 'null'] if (self.is_nullable or self.is_related) else field_type
        template = {"type": field_type_safe_null}

        if self.choices:
            template = {**template, 'enum': self.choices}

        return template

    def string(self):
        template = self.generic()

        if self.max_length is not None:
            template = {**template, 'minLength': 0, 'maxLength': self.max_length}

        return template

    def model(self):
        return self._category.manager.to_schema
