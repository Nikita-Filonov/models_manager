from typing import Union, Type, Dict, List, Callable

from models_manager.constants import TYPE_NAMES
from models_manager.manager.exeptions import FieldException
from models_manager.providers.context import ProviderContext
from models_manager.providers.provider import CommonProvider, Provider


class Field:
    SUPPORTED_TYPES = (str, int, float, list, dict, bool)
    SUPPORTED_TYPES_ANNOTATION = Union[str, int, float, list, dict, bool, Callable, None]

    def __init__(self, json: str = None,
                 max_length: int = None,
                 null: bool = False,
                 only_json: bool = False,
                 is_related: bool = False,
                 value: SUPPORTED_TYPES_ANNOTATION = None,
                 category: Union[Type[str], Type[int], Type[float], Type[list], Type[dict], Type[bool]] = str,
                 default: SUPPORTED_TYPES_ANNOTATION = None):
        self.json = json
        self.null = null
        self.value = value
        self.max_length = max_length
        self.default = default
        self.only_json = only_json
        self.category = category
        self.is_related = is_related

    @property
    def get_value(self) -> SUPPORTED_TYPES_ANNOTATION:
        """
        Returns ``value`` attribute if it is not None, else
        will return default value

        Example:
        >>> name = Field(json='name', category=str, default='some')
        >>> name.get_value
        'some'

        >>> name = Field(json='name', category=str, default='some', value='another')
        >>> name.get_value
        'another'

        >>> name = Field(json='name', category=str, value='another')
        >>> name.get_value
        'another'
        """
        return self.get_default if self.value is None else self.value

    @property
    def get_default(self) -> SUPPORTED_TYPES_ANNOTATION:
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
        if not issubclass(self.category, self.SUPPORTED_TYPES):
            raise FieldException(f'Category type of "{self.category}" is not supported.')

        if self.default is None:
            return

        return self.category(self.default() if callable(self.default) else self.default)

    def __str__(self):
        return str(self.get_value)

    def __repr__(self):
        return str(self.get_value)

    def __add__(self, other):
        return self.get_value + other

    def __len__(self):
        return len(self.get_value)

    @property
    def is_nullable(self):
        return self.null

    @property
    def ignore_json(self):
        return self.json

    @property
    def get_schema(self) -> Union[Dict[str, int], Dict[str, Union[List[str], str]]]:
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
        field_type = [TYPE_NAMES[self.category], 'null'] \
            if (self.is_nullable or self.is_related) else TYPE_NAMES[self.category]
        template = {"type": field_type}

        if (self.category is str) and (self.max_length is not None):
            template = {**template, 'minLength': 0, 'maxLength': self.max_length}

        return template

    def get_negative_values(self, provider: Provider = None) -> SUPPORTED_TYPES:
        """
        :param provider: Provider class which will be applied for getting negative value
        :return: Negative value depends on Field context

        Should be used to get negative value of the Field

        Example:
            >>> name = Field(json='name', category=str, max_length=255, null=False)
            >>> name.get_negative_values()
        """
        safe_provider = provider or CommonProvider
        value_method = getattr(safe_provider, TYPE_NAMES[self.category])
        context = ProviderContext(null=self.is_nullable, max_length=self.max_length)

        return value_method(context)
