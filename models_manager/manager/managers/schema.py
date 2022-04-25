from typing import Dict, Union, List

from models_manager.manager.managers.base import BaseManager


class SchemaManager(BaseManager):
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
        return {
            "title": self._model,
            "type": "object",
            "properties": {
                field.json: field.get_schema for _, field in original_fields
                if field.json is not None
            },
            "required": [
                value.json for _, value in original_fields
                if (value.json is not None) and (not value.is_optional) and (not value.is_related)
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
