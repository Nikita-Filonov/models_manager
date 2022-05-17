from copy import deepcopy
from typing import Union, Any

from models_manager import Model
from models_manager.manager.exeptions import JsonException
from models_manager.manager.model import Meta
from models_manager.schema.schema_template import SchemaTemplate
from models_manager.schema.validator import SchemaValidator


class JsonProvider:
    def __init__(self, schema_template: SchemaTemplate, original_value, json_key=True, inner=False):
        self._json_key = json_key
        self._schema_template = schema_template
        self._original_value = original_value if inner else deepcopy(original_value)

        self._args = self._schema_template.args
        self._inner = self._schema_template.inner
        self._origin = self._schema_template.origin

    def _analyze_model(self, value: Union[Any, Model], key=None):
        if isinstance(value, Model):
            if key is None:
                self._original_value = value.manager.to_dict(json_key=self._json_key)
            else:
                self._original_value[key] = value.manager.to_dict(json_key=self._json_key)

        try:
            if issubclass(value, Model):
                if key is None:
                    self._original_value = value.manager.to_dict(json_key=self._json_key)
                else:
                    self._original_value[key] = value.manager.to_dict(json_key=self._json_key)
        except TypeError:
            pass

    def _go_for_dict(self):
        if not hasattr(self._original_value, 'items'):
            raise JsonException(f'Unable to resolve "{self._original_value}" as Object')

        for key, value in self._original_value.items():
            self._analyze_model(value=value, key=key)

            if self._inner:
                inner_value = JsonProvider(self._inner, value, inner=True).get_value()
                self._original_value[key] = inner_value

    def _go_for_list(self):
        for index, value in enumerate(self._original_value):
            self._analyze_model(value=value, key=index)

            if self._inner:
                inner_value = JsonProvider(self._inner, value, inner=True).get_value()
                self._original_value[index] = inner_value

    def _go_for_union(self):
        self._analyze_model(value=self._original_value)

    def get_value(self):
        if self._origin == SchemaValidator.UNION:
            self._go_for_union()
            return self._original_value

        if issubclass(self._origin, dict):
            self._go_for_dict()

        if issubclass(self._origin, list):
            self._go_for_list()

        if isinstance(self._origin, Meta):
            self._analyze_model(self._original_value)

        return self._original_value
