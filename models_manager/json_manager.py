import logging
from typing import Dict, List, Union, Tuple

from models_manager.field import Field
from models_manager.providers.provider import Provider


class JsonManager:
    """
    models manager.

    Example usage:

    class MyModel(Model):
        ...

    my_model = MyModel.manager.to_json
    """

    def __init__(self, model, mro, **kwargs):
        self._model = model
        self._mro = mro
        self.__resolve_attrs(**kwargs)

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
                setattr(self, f'_meta__{field}', value)
                continue

            setattr(self, field, value)

    @property
    def __fields_as_original(self) -> Dict[str, Field]:
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
            field.replace('_meta__', ''): value
            for field, value in self.__dict__.items()
            if field.startswith('_meta')
        }

    @property
    def __only_db_attrs(self) -> dict:
        """
        Filters model fields and removes fields with only_json=True
        property. This needed because some model fields are different from
        what API required.

        Example:
        class MyModel(Model):
           id: int = Field(default=1)
           last_name: str = Field(default='some_last_name')
           username: str = Field(default='some', only_json=True)

        In this example "username" will be ignored when creating model from database
        """
        return {
            field: value
            for field, value in self.__fields_as_original.items()
            if not value.only_json
        }

    @property
    def to_json(self) -> dict:
        """
        Returns json payload. To return field in json,
        json property: Field(json='some_value'), should be
        defined.

        Example:
        MyModel.manager.to_json -> {'id': 1, 'username': 'some'}
        """
        return {
            value.json: value.get_default
            for value in self.__fields_as_original.values()
            if value.json is not None
        }

    def to_negative_json(self, fields: Union[List[Field], Tuple[Field]] = None, provider: Provider = None) -> dict:
        """
        Same as .to_json, but will return json with negative values

        :param fields: List or tuple of fields that should be returned with negative values.
        By default if fields = None, all fields will be returned with negative values
        :param provider: Provider class that will be applied for all fields
        :return: Dictionary

        Example:
            class MyModel(Model):
                id = Field(default=1, json='id')
                username = Field(json='username', default='some', category=str, null=False)

            MyModel.manager.to_negative_json(fields=[MyModel.username]) -> {'id': '1', 'username': None}
        """
        fields_as_original = self.__fields_as_original.values()
        safe_fields = fields or fields_as_original
        return {
            value.json: value.get_negative_values(provider) if value in safe_fields else value.get_default
            for value in fields_as_original
            if value.json is not None
        }

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
        original_fields = self.__fields_as_original.items()
        return {
            "type": "object",
            "properties": {
                field.json: field.get_schema for _, field in original_fields
                if field.json is not None
            },
            "required": [
                value.json for key, value in original_fields
                if (value.json is not None) and (not value.is_related)
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

    def related_fields(self, as_json=True) -> List[str]:
        """
        Returns model related fields. To mark field related,
        set is_related to True.

        Example:
        class MyModel(Model):
           id: int = Field(default=1)
           last_name: str = Field(default='some_last_name')
           username: str = Field(default='some', json='Username', is_related=True)

        MyModel.manager.related_fields(as_json=True) -> ['Username']
        MyModel.manager.related_fields(as_json=False) -> ['username']
        """
        return [
            value.json if as_json else key
            for key, value in self.__fields_as_original.items()
            if value.is_related
        ]
