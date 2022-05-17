import logging
from typing import Dict, List, Union

from models_manager.connect import Connect
from models_manager.manager.exeptions import ModelDoesNotExists, ModelOperationError
from models_manager.manager.field.field import Field
from models_manager.manager.managers.base import BaseManager
from models_manager.manager.query.builder import get_query
from models_manager.manager.query_set import QuerySet
from models_manager.utils import normalize_model, serializer, dump_value, dump_fields, binding

connection = Connect()


class DatabaseManager(BaseManager):

    @property
    def _lazy_query(self):
        return getattr(connection, self._database, None)

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
            for field, value in self._fields_as_original().items()
            if not value.only_json
        }

    def __as_json(self, as_json, result) -> Union[QuerySet, 'DatabaseManager']:
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
                type(self._model, self._mro, self._resolve_attrs(**{**self.__dict__, **(row or {})}, is_lazy=True))()
                for row in result
            ]
            return QuerySet(self._model, self._identity, self._lazy_query, self._mro, instances, self)

        payload = {**self.__dict__, **(result or {})}
        return type(self._model, self._mro, self._resolve_attrs(**payload, is_lazy=True))()

    def fields(self, json_key: bool = True) -> Dict[str, Field]:
        return self._fields_as_original(json_key)

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
            for key, value in self._fields_as_original().items()
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

    def get(self, *args, as_json=True, **kwargs):
        """
        Getting db instance

        Example:
        MyModel.manager.get(id=1) -> {'id': 1, 'username': 'some'}
        MyModel.manager.get(id=1, as_json=False) -> <class '__main__.Activities'>
        """
        model = normalize_model(self._model)
        sql = f'SELECT * FROM "{model}"'

        query = get_query(model, *args, **kwargs)
        if query:
            sql += f' WHERE {query}'

        cursor = self._lazy_query(sql)
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
        self._lazy_query(sql, (self.__dict__[self._identity].value,))

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

        cursor = self._lazy_query(sql, (self.__dict__[self._identity].value,))
        result = serializer(cursor)

        return self.__as_json(as_json, result)

    def filter(self, *args, as_json=True, **kwargs):
        """
        Getting db instances

        Example:
        MyModel.manager.filter(id=1) -> [{'id': 1, 'username': 'some'}]
        MyModel.manager.filter(id=1, as_json=False) -> [<class '__main__.Activities'>]
        """
        model = normalize_model(self._model)
        sql = f'SELECT * FROM "{model}"'
        values = tuple(kwargs.values())
        query = get_query(model, *args, **kwargs)

        if query:
            sql += f' WHERE {query}'

        if isinstance(values, (list, tuple)):
            if not all(bool(value) for value in values):
                logging.warning(f'Values is empty {values}({type(values)}). Nothing to query')
                return self.__as_json(as_json, [])

        cursor = self._lazy_query(sql)
        result = serializer(cursor, many=True)

        return self.__as_json(as_json, result)

    def is_exists(self, *args, **kwargs) -> bool:
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
        query = get_query(model, *args, **kwargs)

        if query:
            sql += f' WHERE {query}'

        cursor = self._lazy_query(sql)
        return bool(cursor.fetchall())

    def get_or_create(self, *args, as_json=True, **kwargs):
        """
        Will return existing instance if such exists else
        will create such instance and return it.

        Example:
        MyModel.manager.get_or_create(name='some') -> {'id': 1, 'name': 'some'}
        """
        try:
            return self.get(as_json=as_json, *args, **kwargs)
        except ModelDoesNotExists:
            return self.create(as_json, **kwargs)
