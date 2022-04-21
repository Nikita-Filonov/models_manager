from typing import Union, Dict, List

from models_manager.manager.exeptions import FieldException
from models_manager.manager.field.typing import GenericTypes, GenericCategories, SUPPORTED_TYPES, GenericChoices
from models_manager.providers.provider import Provider, NegativeValuesProvider
from models_manager.schema.schema_typing import resolve_typing


class Field:

    def __init__(self, json: str = None,
                 title: str = None,
                 description: str = None,
                 max_length: int = None,
                 min_length: int = None,
                 max_items: int = None,
                 min_items: int = None,
                 gt: float = None,
                 ge: float = None,
                 lt: float = None,
                 le: float = None,
                 null: bool = False,
                 only_json: bool = False,
                 is_related: bool = False,
                 related_to=None,
                 optional: bool = False,
                 value: GenericTypes = None,
                 choices: GenericChoices = None,
                 category: GenericCategories = str,
                 default: GenericTypes = None):
        self.json = json
        self.null = null
        self._value = value
        self.gt = gt
        self.ge = ge
        self.lt = lt
        self.le = le
        self.max_length = max_length
        self.min_length = min_length
        self.max_items = max_items
        self.min_items = min_items
        self.title = title
        self.description = description
        self.default = default
        self.only_json = only_json
        self.category = category
        self.is_related = is_related
        self.choices = choices
        self.related_to = related_to
        self.optional = optional

    @property
    def value(self) -> GenericTypes:
        """
        Returns ``value`` attribute if it is not None, else
        will return default value

        Example:
        >>> name = Field(json='name', category=str, default='some')
        >>> name.value
        'some'

        >>> name = Field(json='name', category=str, default='some', value='another')
        >>> name.value
        'another'

        >>> name = Field(json='name', category=str, value='another')
        >>> name.value
        'another'
        """
        return self.get_default if self._value is None else self._value

    @value.setter
    def value(self, value):
        if self.choices and value not in self.choices:
            choices = ', '.join(map(str, self.choices))
            raise FieldException(f'The "{self.json}" field must be one of the {choices}, but {value} was received')

        self._value = self.category(value)

    @property
    def get_default(self) -> GenericTypes:
        """
        Returns ``default`` attribute. There is two possible scenarios:
        1. ``default`` is a function - ``get_default`` will call this function and
        will return returned value by function.
        2. ``default`` is a string, integer etc. - will return ``default`` attribute.

        For both scenarios we are applying ``category`` type to the returned value.
        Basically it might look like:
        >>> default='some'
        >>> category = str
        >>> category(default)
        'some'

        Example:
        >>> name = Field(category=str, default='some')
        >>> name.get_default
        'some'

        >>> some = lambda: 'some'
        >>> name = Field(category=str, default=some)
        >>> name.get_default
        'some'

        In fact this will also work
        >>> some = lambda: []
        >>> name = Field(category=str, default=some)
        >>> name.get_default
        '[]'

        >>> some = lambda: []
        >>> name = Field(category=list, default=some)
        >>> name.get_default
        []

        """
        if not issubclass(self.category, SUPPORTED_TYPES):
            raise FieldException(f'Category type of "{self.category}" is not supported.')

        if self.default is None:
            return

        return self.category(self.default() if callable(self.default) else self.default)

    def __str__(self):
        return f'<Field: {self.value}>'

    def __repr__(self):
        return f'<Field: {self.value}>'

    def __add__(self, other):
        return self.value + other

    def __len__(self):
        return len(self.value)

    @property
    def is_nullable(self):
        return self.null

    @property
    def ignore_json(self):
        return self.json

    @property
    def is_optional(self) -> bool:
        return self.optional

    @property
    def get_schema(self) -> Union[Dict[str, int], Dict[str, Union[list, tuple]], Dict[str, Union[List[str], str]]]:
        """
        Used to get schema properties template for certain field.

        Example:
        >>> name = Field(json='name', category=str, max_length=255, null=True)
        >>> name.get_schema
        {'type': ['string', 'null'], 'minLength': 0, 'maxLength': 255}

        >>> username = Field(json='username', category=str, max_length=255, null=False)
        >>> username.get_schema
        {'type': 'string', 'minLength': 0, 'maxLength': 255}

        >>> email = Field(json='email', category=str, null=False)
        >>> email.get_schema
        {'type': 'string'}

        >>> project_id = Field(json='projectId', category=str, null=False, is_related=True)
        >>> project_id.get_schema
        {'type': ['string', 'null']}

        >>> object_id = Field(json='projectId', category=str, is_related=True)
        >>> object_id.get_schema
        {'type': ['string', 'null']}
        """
        from models_manager.schema.provider import SchemaProvider  # no qa

        schema_template = resolve_typing(self.category)
        schema_provider = SchemaProvider(
            schema_template=schema_template,
            choices=self.choices,
            max_length=self.max_length,
            min_length=self.min_length,
            gt=self.gt,
            ge=self.ge,
            lt=self.lt,
            le=self.le,
            max_items=self.max_items,
            min_items=self.min_items,
            title=self.title,
            description=self.description
        )
        return schema_provider.get_schema()

    def get_negative_values(self, provider: Provider = None) -> GenericTypes:
        """
        :param provider: Provider class which will be applied for getting negative value
        :return: Negative value depends on Field context

        Should be used to get negative value of the Field

        Example:
            >>> name = Field(json='name', category=str, max_length=255, null=False)
            >>> name.get_negative_values()
        """
        safe_provider = provider or NegativeValuesProvider
        return safe_provider(
            null=self.null,
            max_length=self.max_length,
            category=self.category,
            json=self.json
        ).value()
