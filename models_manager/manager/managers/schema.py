from itertools import tee
from typing import Dict, Union, List

from models_manager.manager.managers.base import BaseManager
from models_manager.utils import get_json_from_fields


class SchemaManager(BaseManager):

    def __init__(self, model, mro, **kwargs):
        super().__init__(model, mro, **kwargs)

        self._exclude_schema = None

    @property
    def exclude_schema(self):
        return get_json_from_fields(self._exclude_schema)

    @exclude_schema.setter
    def exclude_schema(self, value):
        self._exclude_schema = value

    @property
    def to_schema(self) -> Dict[str, Union[str, dict, List[str]]]:
        """
        Returns model schema based on its "category" types.
        This method can be used to check model schema.

        If you want to add schema to model field you have to define two keywords
        into Field class:
        - json: string
        - category: any of available types str, int, float, dict, list, bool

        Example:
        class MyModel(Model):
            id = Field(default=1, json='id', category=str)
            last_name = Field(default='some_last_name', json='last_name', category=str)
            is_active = Field(default=True, json='is_active', category=bool)
            username = Field(default='some', category=str)

        MyModel.manager.to_schema -> will return following template:

        {
            'type': 'object',
            'properties':
                {
                    'id': {'type': 'string'},
                    'last_name': {'type': 'string'},
                    'is_active': {'type': 'boolean'}
                }
        }

        Then this template can be used in test, for example:

        class MyModel(Model):
             id = Field(default=1, json='id', category=str)
             last_name = Field(default='some_last_name', json='last_name', category=str)
             is_active = Field(default=True, json='is_active', category=bool)
             username = Field(default='some', category=str)

        from jsonschema import validate
        schema = MyModel.manager.to_schema
        json = MyModel.manager.to_json

        # If no exception is raised by validate(), the instance is valid.
        validate(instance=json, schema=schema)
        """
        original_fields = self._fields_as_original().items()
        properties, required = tee(filter(lambda args: args[1].json not in self.exclude_schema, original_fields))

        return {
            "title": self._model,
            "type": "object",
            "properties": {
                field.json: field.get_schema for _, field in properties
                if field.json is not None
            },
            "required": [
                field.json for _, field in required
                if (field.json is not None) and (not field.is_optional)
            ]
        }

    @property
    def to_array_schema(self) -> Dict[str, Union[str, Dict[str, Union[str, dict, List[str]]]]]:
        """
        Can be used to check schema in list.

        Example:

        class MyModel(Model):
            id = Field(default=1, json='id', category=int)
            name = Field(default='some', json='name', category=str)

        some_list = [
            {'id': 1, 'name': 'some'},
            {'id': 2, 'name': 'other'}
        ]
        MyModel.manager.to_array_schema ->
        {
            'type': 'array',  <- this means we checking array
            'items': { <- describe how the object should look
                'type': 'object',
                'properties': {
                    'id': {'type': 'number'},
                    'name': {'type': 'string'}
                },
                'required': ['id', 'name']
            }
        }
        """
        return {"type": "array", "items": self.to_schema}
