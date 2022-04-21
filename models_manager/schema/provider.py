from models_manager.constants import TYPE_NAMES
from models_manager.manager.exeptions import SchemaException
from models_manager.manager.field.typing import GenericChoices
from models_manager.manager.model import Meta
from models_manager.schema.schema_typing import ORIGIN, ARGS, INNER


class SchemaProvider:
    UNION = 'union'
    ANY_OF = 'anyOf'
    ITEMS = 'items'
    ADDITIONAL_PROPERTIES = 'additionalProperties'
    MIN_ITEMS = 'minItems'
    MAX_ITEMS = 'maxItems'

    def __init__(
            self,
            schema_template: dict,
            choices: GenericChoices = None,
            max_length: int = None,
            min_length: int = None,
            gt: float = None,
            ge: float = None,
            lt: float = None,
            le: float = None,
            max_items: int = None,
            min_items: int = None,
    ):
        self._schema_template = schema_template
        self._template = {}

        self._choices = choices
        self._max_length = max_length
        self._min_length = min_length
        self._max_items = max_items
        self._min_items = min_items
        self._gt = gt
        self._ge = ge
        self._lt = lt
        self._le = le

        self._args = self._schema_template.get(ARGS)
        self._inner = self._schema_template.get(INNER)
        self._origin = self._schema_template.get(ORIGIN)

    def __apply_default_values(self):
        if self._choices is not None:
            self._template['enum'] = self._choices

        if self._max_length is not None:
            self._template['maxLength'] = self._max_length

        if self._min_length is not None:
            self._template['minLength'] = self._min_length

        if (self._gt is not None) and (self._ge is not None):
            raise SchemaException('Properties "gt" and "ge" can not be used at the same time')

        if self._gt is not None:
            self._template['exclusiveMinimum'] = self._gt

        if self._ge is not None:
            self._template['minimum'] = self._ge

        if (self._lt is not None) and (self._le is not None):
            raise SchemaException('Properties "lt" and "le" can not be used at the same time')

        if self._lt is not None:
            self._template['exclusiveMaximum'] = self._lt

        if self._le is not None:
            self._template['maximum'] = self._le

    @classmethod
    def __get_type(cls, original_type):
        type_name = TYPE_NAMES.get(original_type, None)
        if type_name is not None:
            return type_name

        if isinstance(original_type, Meta):
            return cls({ORIGIN: original_type}).get_schema()

        return 'null'

    def __safely_get_type(self, original_type):
        if TYPE_NAMES.get(original_type):
            return {'type': self.__get_type(original_type)}

        return self.__get_type(original_type)

    def __go_for_object(self):
        if (not self._args) and (len(self._args) != 2):
            return

        if self._inner:
            inner_template = SchemaProvider(self._inner).get_schema()
            self._template[self.ADDITIONAL_PROPERTIES] = inner_template
        else:
            self._template[self.ADDITIONAL_PROPERTIES] = self.__safely_get_type(self._args[1])

    def __go_for_array(self):
        self._template[self.ITEMS] = {}

        if self._inner:
            self._template[self.ITEMS] = SchemaProvider(self._inner).get_schema()

        if self._args:
            self._template[self.ITEMS] = self.__safely_get_type(self._args[0])

    def __go_for_tuple(self):
        if (self._min_items is not None) or (self._max_items is not None):
            raise SchemaException('Properties "min_items" and "max_items" can not be used with "tuple"')

        if self._inner:
            self._template[self.ITEMS] = SchemaProvider(self._inner).get_schema()

        if self._args:
            self._template[self.MIN_ITEMS] = len(self._args)
            self._template[self.MAX_ITEMS] = len(self._args)
            self._template[self.ITEMS] = [self.__safely_get_type(arg) for arg in self._args]

    def __go_for_union(self):
        self._template[self.ANY_OF] = [self.__safely_get_type(arg) for arg in self._args]

        if self._inner:
            inner_template = SchemaProvider(self._inner).get_schema()
            self._template[self.ANY_OF] = [*self._template[self.ANY_OF], inner_template]

        return self._template

    def __go_for_model(self):
        self._template = self._origin.manager.to_schema

    def get_schema(self):
        self.__apply_default_values()

        type_name = TYPE_NAMES.get(self._origin, None)
        if type_name is not None:
            self._template['type'] = TYPE_NAMES[self._origin]

        if self._origin is None:
            return self._template

        if self._origin == self.UNION:
            return self.__go_for_union()

        if isinstance(self._origin, Meta):
            self.__go_for_model()

        if issubclass(self._origin, list):
            self.__go_for_array()

        if issubclass(self._origin, tuple):
            self.__go_for_tuple()

        if issubclass(self._origin, dict):
            self.__go_for_object()

        return self._template
