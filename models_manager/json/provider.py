from copy import deepcopy
from typing import Union, Any

from models_manager import Model
from models_manager.manager.model import Meta
from models_manager.schema.schema_typing import ARGS, INNER, ORIGIN


class JsonProvider:
    def __init__(self, schema_template: dict, original_value, inner=False):
        self._schema_template = schema_template
        self._original_value = original_value if inner else deepcopy(original_value)

        self._args = self._schema_template.get(ARGS)
        self._inner = self._schema_template.get(INNER)
        self._origin = self._schema_template.get(ORIGIN)

    def _analyze_model(self, value: Union[Any, Model], key=None):
        if isinstance(value, Model):
            if key is None:
                self._original_value = value.manager.to_json
            else:
                self._original_value[key] = value.manager.to_json

        try:
            if issubclass(value, Model):
                if key is None:
                    self._original_value = value.manager.to_json
                else:
                    self._original_value[key] = value.manager.to_json
        except TypeError:
            pass

    def _go_for_dict(self):
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
        if self._origin == 'union':
            self._go_for_union()
            return self._original_value

        if issubclass(self._origin, dict):
            self._go_for_dict()

        if issubclass(self._origin, list):
            self._go_for_list()

        if isinstance(self._origin, Meta):
            self._analyze_model(self._original_value)

        return self._original_value
