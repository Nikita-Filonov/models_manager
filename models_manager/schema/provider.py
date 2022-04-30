from models_manager.constants import TYPE_NAMES
from models_manager.manager.exeptions import SchemaException
from models_manager.manager.field.typing import GenericChoices
from models_manager.manager.model import Meta
from models_manager.schema.context import SchemaContext
from models_manager.schema.schema_template import SchemaTemplate
from models_manager.schema.validator import SchemaValidator


class SchemaProvider(SchemaValidator):
    """
    Base schema provider. Used to generate schema template
    based on provided attributes.

    Basically ``SchemaProvider`` only need ``schema_template`` to generate
    some schema template. Format of ``schema_template`` must look like:
    - {'origin': dict, 'args': []}
    - {'origin': dict, 'args': [str, int]}
    - {'origin': list, 'args': [], 'inner': {'origin': dict, 'args': [str, int]}}

    Example:
        >>> from models_manager.schema.schema_typing import resolve_typing
        >>> template = resolve_typing(dict)
        >>> SchemaProvider(schema_template=template).get_schema()
        {'type': 'object'}

        >>> from models_manager.schema.schema_typing import resolve_typing
        >>> from typing import Dict
        >>> template = resolve_typing(Dict[str, int])
        >>> SchemaProvider(schema_template=template).get_schema()
        {'additionalProperties': {'type': 'number'}, 'type': 'object'}
    """

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
            description: str = None,
    ):
        super().__init__(
            schema_template=schema_template,
            choices=choices,
            max_length=max_length,
            min_length=min_length,
            gt=gt,
            ge=ge,
            lt=lt,
            le=le,
            max_items=max_items,
            min_items=min_items,
            pattern=pattern,
            title=title,
            description=description
        )

        self._template = {}
        self._context = SchemaContext()

        self._args = self._schema_template.args
        self._inner = self._schema_template.inner
        self._origin = self._schema_template.origin

    def __validate_default_values(self):
        self._validate_for_common()
        self._validate_for_int_float()
        self._validate_for_str()
        self._validate_for_list_tuple()

    def __apply_default_values(self):
        self._context.title = self._title
        self._context.description = self._description
        self._context.pattern = self._pattern
        self._context.choices = self._choices
        self._context.max_length = self._max_length
        self._context.min_length = self._min_length
        self._context.gt = self._gt
        self._context.ge = self._ge
        self._context.lt = self._lt
        self._context.le = self._le
        self._context.min_items = self._min_items
        self._context.max_items = self._max_items

        origin_format = self._context.FORMATS.get(self._origin)
        if origin_format is not None:
            self._context.format = origin_format

    @classmethod
    def __get_type(cls, original_type):
        type_name = TYPE_NAMES.get(original_type, None)
        if type_name is not None:
            return type_name

        if isinstance(original_type, Meta):
            template = SchemaTemplate()
            template.origin = original_type
            return cls(template).get_schema()

        return {SchemaContext.TYPE: SchemaContext.NULL}

    def __safely_get_type(self, original_type):
        if TYPE_NAMES.get(original_type):
            context = SchemaContext(type=self.__get_type(original_type))
            return context.template

        return self.__get_type(original_type)

    def _go_for_object(self):
        if (not self._args) and (len(self._args) != 2):
            return

        if self._inner:
            inner_template = SchemaProvider(self._inner).get_schema()
            self._context.additional_properties = inner_template
        else:
            self._context.additional_properties = self.__safely_get_type(self._args[1])

    def _go_for_array(self):
        self._context.items = {}

        if self._inner:
            self._context.items = SchemaProvider(self._inner).get_schema()

        if self._args:
            self._context.items = self.__safely_get_type(self._args[0])

    def _go_for_tuple(self):
        if (self._min_items is not None) or (self._max_items is not None):
            raise SchemaException('Properties "min_items" and "max_items" can not be used with "tuple"')

        if self._inner:
            self._context.items = SchemaProvider(self._inner).get_schema()

        if self._args:
            self._context.min_items = self._min_items or len(self._args)
            self._context.max_items = self._max_items or len(self._args)
            self._context.items = [self.__safely_get_type(arg) for arg in self._args]

    def _go_for_union(self):
        self._context.any_of = [self.__safely_get_type(arg) for arg in self._args]

        if self._inner:
            inner_template = SchemaProvider(self._inner).get_schema()
            self._context.any_of = [*self._context.any_of, inner_template]

        return self._context.template

    def _go_for_model(self):
        self._context.template = self._origin.manager.to_schema

    def get_schema(self):
        self.__validate_default_values()
        self.__apply_default_values()

        type_name = TYPE_NAMES.get(self._origin, None)
        if type_name is not None:
            self._context.type = TYPE_NAMES[self._origin]

        if self._origin is None:
            return self._context.template

        if self._origin == self.UNION:
            return self._go_for_union()

        if isinstance(self._origin, Meta):
            self._go_for_model()

        if issubclass(self._origin, list):
            self._go_for_array()

        if issubclass(self._origin, tuple):
            self._go_for_tuple()

        if issubclass(self._origin, dict):
            self._go_for_object()

        return self._context.template
