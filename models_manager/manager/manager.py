import logging
from typing import Dict, List, Union, Tuple

from models_manager.connect import Connect
from models_manager.manager.exeptions import ModelDoesNotExists, ModelOperationError
from models_manager.manager.field import Field
from models_manager.manager.query import QuerySet
from models_manager.providers.provider import Provider
from models_manager.utils import where, normalize_model, serializer, dump_value, dump_fields, binding

connection = Connect()


class ModelManager:
    """
    Models manager.

    Example usage:

    class MyModel(Model):
        ...

    my_model = MyModel.manager.to_json
    """

    def __init__(self, model, mro, **kwargs):
        self._model = model
        self._mro = mro
        self._identity = kwargs.get('identity')
        self.__resolve_attrs(**kwargs)

        self._database = kwargs.get('database')

    @property
    def _lazy_query(self):
        return getattr(connection, self._database, None)

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

    def __fields_as_original(self, json_key: bool = False) -> Dict[str, Field]:
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
            for field, value in self.__fields_as_original().items()
            if not value.only_json
        }

    def __as_json(self, as_json, result) -> Union[QuerySet, 'ModelManager']:
        """
        Result constructor. Makes result depending on 'as_json' param.
        - If as_json=True will return dict.
        - If as_json=False will return model object, which will have all
        method and attributes of Manager and Model.
        """
        if as_json:
            return result

        if isinstance(result, list):
            instances = [
                type(self._model, self._mro, {**self.__dict__, **(row or {})})()
                for row in result
            ]
            return QuerySet(self._model, self._identity, self._lazy_query, self._mro, instances)

        return type(self._model, self._mro, {**self.__dict__, **(result or {})})()

    def fields(self, json_key: bool) -> Dict[str, Field]:
        return self.__fields_as_original(json_key)

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
            for value in self.__fields_as_original().values()
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
        fields_as_original = self.__fields_as_original().values()
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
        original_fields = self.__fields_as_original().items()
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
            for key, value in self.__fields_as_original().items()
            if value.is_related
        ]

    def db_values(self, **kwargs) -> list:

        """
        Getting model default values and skip only_json fields

        Example:
        class MyModel(Model):
           id: int = Field(default=1)
           last_name: str = Field(default='some_last_name')
           username: str = Field(default='some', only_json=True)
           password: str = Field()

        MyModel.manager.db_values -> [1, 'some_last_name', None]
        """
        values = []
        for key, value in self.__only_db_attrs.items():
            if key in kwargs.keys():
                values.append(kwargs[key])
                continue

            if getattr(value, 'default', None) is not None:
                db_value = str(value.default()) if callable(value.default) else value.default
                values.append(db_value)
                continue

            values.append(None)

        return values

    def db_fields(self, *args, **kwargs) -> list:
        """
        Getting model fields and skip only_json fields

        Example:
        class MyModel(Model):
           id: int = Field(default=1)
           last_name: str = Field(default='some_last_name')
           username: str = Field(default='some', only_json=True)
           password: str = Field()

        MyModel.manager.db_fields() -> ['id', 'last_name', 'password']
        MyModel.manager.db_fields('id', 'last_name') -> ['id', 'last_name']
        """
        fields = list(self.__only_db_attrs)

        if args:
            return list(filter(lambda f: f in args or kwargs, fields))

        return fields

    def get(self, as_json=True, **kwargs):
        """
        Getting db instance

        Example:
        MyModel.manager.get(id=1) -> {'id': 1, 'username': 'some'}
        MyModel.manager.get(id=1, as_json=False) -> <class '__main__.Activities'>
        """
        model = normalize_model(self._model)
        sql = f'SELECT * FROM "{model}"'
        values = tuple(kwargs.values())

        if kwargs:
            bind = ' AND '.join([f'"{model}"."{field}" = %s' for field in kwargs])
            sql += f' WHERE {bind};'

        cursor = self._lazy_query(sql, values)
        result = serializer(cursor, many=False)

        if not result:
            raise ModelDoesNotExists(f'"{self._model}" with {kwargs} does not exists')

        return self.__as_json(as_json, result)

    def create(self, as_json=True, **kwargs):
        model = normalize_model(self._model)
        fields = self.db_fields()
        values = self.db_values(**kwargs)

        for key, value in kwargs.items():
            index = fields.index(key)
            values[index] = value

        sql = f'INSERT INTO "{model}" ({dump_fields(fields)}) VALUES ({binding(values)}) RETURNING *;'

        cursor = self._lazy_query(sql, values)
        result = serializer(cursor)

        return self.__as_json(as_json, result)

    def delete(self):
        """
        Used to delete single instance

        Example:

        some = MyModel.manager.get(id=1, as_json=False)
        some.manager.delete()
        """
        model = normalize_model(self._model)
        sql = f'DELETE FROM "{model}" WHERE "{model}"."{self._identity}" = %s;'
        self._lazy_query(sql, (self.__dict__[self._identity],))

    def update(self, as_json=True, **kwargs):
        """
        Used to update single instance

        Example:

        some = MyModel.manager.get(id=1, as_json=False)
        some.manager.update(Name='New Name', as_json=False) -> <MyModel object>
        either
        some.manager.update(Name='New Name', as_json=False) -> {'id':1, 'Name':'New Name'...}
        """
        if not kwargs:
            raise ModelOperationError(
                'You should provide at least one field to update. '
                'Example .update(Name="Some")'
            )
        model = normalize_model(self._model)
        values = ', '.join([f'"{key}" = {dump_value(value)}' for key, value in kwargs.items()])

        sql = f'UPDATE "{model}" SET {values} WHERE "{model}"."{self._identity}" = %s RETURNING*;'

        cursor = self._lazy_query(sql, (self.__dict__[self._identity],))
        result = serializer(cursor)

        return self.__as_json(as_json, result)

    def filter(self, as_json=True, operand='AND', operator='=', **kwargs):
        """
        Getting db instances

        Example:
        MyModel.manager.filter(id=1) -> [{'id': 1, 'username': 'some'}]
        MyModel.manager.filter(id=1, as_json=False) -> [<class '__main__.Activities'>]
        """
        model = normalize_model(self._model)
        sql = f'SELECT * FROM "{model}"'
        values = tuple(kwargs.values())

        if kwargs:
            sql += where(model, operand, operator, **kwargs)

        if isinstance(values, (list, tuple)):
            if not all(bool(value) for value in values):
                logging.warning(f'Values is empty {values}({type(values)}). Nothing to query')
                return self.__as_json(as_json, [])

        cursor = self._lazy_query(sql, values)
        result = serializer(cursor, many=True)

        return self.__as_json(as_json, result)

    def is_exists(self, operand='AND', operator='=', **kwargs) -> bool:
        """
        This method used to check if object exists in database.
        Will return True if object exists else will return False.

        Same check can be made with 'filter' method, but it is not recommended!

        Example:
        MyModel.manager.is_exists(id=1) -> True
        MyModel.manager.is_exists(id='random') -> False
        """
        model = normalize_model(self._model)
        sql = f'SELECT NULL FROM "{model}"'
        values = tuple(kwargs.values())

        if kwargs:
            sql += where(model, operand, operator, **kwargs)

        cursor = self._lazy_query(sql, values)
        return bool(cursor.fetchall())

    def get_or_create(self, as_json=True, **kwargs):
        """
        Will return existing instance if such exists else
        will create such instance and return it.

        Example:
        MyModel.manager.get_or_create(name='some') -> {'id': 1, 'name': 'some'}
        """
        try:
            return self.get(as_json, **kwargs)
        except ModelDoesNotExists:
            return self.create(as_json, **kwargs)
