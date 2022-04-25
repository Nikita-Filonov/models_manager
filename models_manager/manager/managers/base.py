import logging
from copy import deepcopy
from typing import Dict

from models_manager import Field


class BaseManager:
    def __init__(self, model, mro, **kwargs):
        self._model = model
        self._mro = mro
        self._identity = kwargs.get('identity')
        self.__resolve_attrs(**kwargs)

        self._database = kwargs.get('database')

    def __resolve_attrs(self, **kwargs):
        """
        Method that helps to keep consistency of attr
        between objects and initialization.

        Original model might look like:
        class MyModel(Model):
           id: int = Field(default=1)
           last_name: str = Field(default='some_last_name')
           username: str = Field(default='some', only_json=True)
           password: str = Field()

        So model attrs will look like:
        {
            'id': 1,
            'last_name': 'some_last_name',
            ...
            '_meta__id: Field(default='some_last_name')
            '_meta__last_name': Field(default='some', only_json=True),
            ...
        }

        This way each model object will have always the same attrs
        """
        for field, value in kwargs.items():
            if isinstance(value, Field) and field.startswith('_meta'):
                original_field = field.replace('_meta__', '')
                try:
                    kwargs[field].value = kwargs[original_field]
                except KeyError:
                    logging.error(f'Unable to resolve field "{field}". Skipped')

            if isinstance(value, Field) and not field.startswith('_meta'):
                setattr(self, f'_meta__{field}', deepcopy(value))
                continue

            setattr(self, field, value)

    def apply_values(self, **kwargs):
        for _, field in self._fields_as_original(json_key=False).items():
            value = kwargs.get(field.json, None)

            if value is not None:
                field.value = value

    def _fields_as_original(self, json_key: bool = False) -> Dict[str, Field]:
        """
        Returns original model names with their <Field> object.
        So this method converts all _meta* attrs to original
        field name.

        Example:
        class MyModel(Model):
           id: int = Field(default=1)
           last_name: str = Field(default='some_last_name')
           username: str = Field(default='some', only_json=True)
           password: str = Field()

        last_name -> 'some_last_name'
        _meta__last_name -> Field(default='some_last_name')
        __fields_as_original -> {'last_name': Field(default='some_last_name')}
        """
        return {
            ((value.json or field.replace('_meta__', '')) if json_key else field.replace('_meta__', '')): value
            for field, value in self.__dict__.items()
            if field.startswith('_meta')
        }
