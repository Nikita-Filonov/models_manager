from datetime import datetime, date, time, timedelta
from typing import Union, Dict, List, Any
from uuid import UUID

from jsonschema import validate

from models_manager.manager.field.typing import GenericTypes, GenericCategories, GenericChoices
from models_manager.negative.provider import NegativeValuesProvider
from models_manager.providers.provider import Provider, NegativeValuesProviderDeprecated
from models_manager.schema.schema_typing import resolve_typing
from models_manager.utils import deprecated


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
                 pattern: str = None,
                 only_json: bool = False,
                 is_related: bool = False,
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
        self.pattern = pattern
        self.title = title
        self.description = description
        self.default = default
        self.only_json = only_json
        self.category = category
        self.is_related = is_related
        self.choices = choices
        self.optional = optional

        self._typing_template = resolve_typing(self.category)

    def _with_ensure_value_valid(self, value: Any, json_key=True, ignore_validation=False) -> Any:
        from models_manager.json.provider import JsonProvider  # no qa

        provider = JsonProvider(schema_template=self._typing_template, original_value=value, json_key=json_key)
        dict_value = provider.get_value()

        if isinstance(dict_value, (UUID, datetime, date, time, timedelta)):
            dict_value = str(dict_value)

        if not ignore_validation:
            validate(instance=dict_value, schema=self.get_schema)

        return dict_value

    def dict(self, json_key=True, ignore_validation=False):
        """
        Same as ``value`` it returns field current value, but instead of
        ``value`` dict will convert original value into dict, list, string or
        any json serializable object.

        For example we can not serialize/send datetime/date/time object into
        API endpoint. We have to send string, So the ```dict`` will manage such objects

        Examples:
            >>> from typing import Optional
            >>> field = Field(json='field', category=Optional[str])
            >>> field.dict()

            >>> from typing import Optional
            >>> field = Field(json='field', category=Optional[str], default='some')
            >>> field.dict()
            'some'
        """
        return self._with_ensure_value_valid(self.value, json_key=json_key, ignore_validation=ignore_validation)

    @property
    def value(self) -> Any:
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
        if self.json is not None:
            self._with_ensure_value_valid(value)
        self._value = value

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
            []

            >>> some = lambda: []
            >>> name = Field(category=list, default=some)
            >>> name.get_default
            []

        """
        if self.default is None:
            return

        safe_callable_default = self.default() if callable(self.default) else self.default
        return self._with_ensure_value_valid(safe_callable_default)

    def __str__(self):
        if self.json:
            return f'<Field: {self.json}, {self.value}>'
        return f'<Field: {self.value}>'

    def __repr__(self):
        if self.json:
            return f'<Field: {self.json}, {self.value}>'
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
    def negative(self) -> NegativeValuesProvider:
        return NegativeValuesProvider(
            category=self.category,
            choices=self.choices,
            schema_template=self._typing_template,
            max_length=self.max_length,
            min_length=self.min_length,
            max_items=self.max_items,
            min_items=self.min_items,
            gt=self.gt,
            ge=self.ge,
            lt=self.lt,
            le=self.le,
        )

    @property
    def get_schema(self) -> Union[Dict[str, int], Dict[str, Union[list, tuple]], Dict[str, Union[List[str], str]]]:
        """
        Used to get schema properties template for certain field.

        Examples:
            >>> from typing import Optional
            >>> name = Field(json='name', category=Optional[str], max_length=255, null=True)
            >>> name.get_schema
            {'maxLength': 255, 'anyOf': [{'type': 'string'}, {'type': 'null'}]}

            >>> username = Field(json='username', category=str, max_length=255, null=False)
            >>> username.get_schema
            {'maxLength': 255, 'type': 'string'}

            >>> email = Field(json='email', category=str, null=False)
            >>> email.get_schema
            {'type': 'string'}

            >>> project_id = Field(json='projectId', category=str, null=False, is_related=True)
            >>> project_id.get_schema
            {'type': 'string'}

            >>> object_id = Field(json='projectId', category=str, is_related=True)
            >>> object_id.get_schema
            {'type': 'string'}
        """
        from models_manager.schema.provider import SchemaProvider  # no qa

        schema_provider = SchemaProvider(
            schema_template=self._typing_template,
            choices=self.choices,
            max_length=self.max_length,
            min_length=self.min_length,
            gt=self.gt,
            ge=self.ge,
            lt=self.lt,
            le=self.le,
            max_items=self.max_items,
            min_items=self.min_items,
            pattern=self.pattern,
            title=self.title,
            description=self.description
        )
        return schema_provider.get_schema()

    @deprecated('Use "negative" instead')
    def get_negative_values(self, provider: Provider = None) -> GenericTypes:
        """
        :param provider: Provider class which will be applied for getting negative value
        :return: Negative value depends on Field context

        Should be used to get negative value of the Field

        Example:
            >>> name = Field(json='name', category=str, max_length=255, null=False)
            >>> name.get_negative_values()
        """
        safe_provider = provider or NegativeValuesProviderDeprecated
        return safe_provider(
            null=self.null,
            max_length=self.max_length,
            category=self.category,
            json=self.json
        ).value()
