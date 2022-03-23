import logging

from models_manager.manager.exeptions import ModelOperationError, QuerySetOperationError
from models_manager.utils import serializer, normalize_model, binding, dump_value, where


class QuerySet:
    """
    This class used to manage multiple objects.

    Example:

    class MyModel(Model):
        ...

    result = MyModel.manager.filter(name='some', as_json=False) -> QuerySet([...instances...])
    result.update(name='other') -> QuerySet([...instances...])
    result.delete() -> None
    """

    def __init__(self, model, identity, query, mro, instances):
        self._model = model
        self._mro = mro
        self._instances = instances
        self._identity = identity
        self._query = query

        self._index = 0

    def __str__(self):
        objects = ', '.join([str(instance) for instance in self._instances])
        return f'QuerySet([{objects}])'

    def __iter__(self):
        return self

    def __next__(self):
        try:
            result = self._instances[self._index]
        except IndexError:
            raise StopIteration
        self._index += 1
        return result

    def __len__(self):
        return len(self._instances)

    @property
    def __map_to_identity(self) -> tuple:
        """Return tuple of instances identities"""
        try:
            return tuple(getattr(instance, self._identity) for instance in self._instances)
        except TypeError:
            raise QuerySetOperationError(
                'Could not find "identity" attribute. '
                'Did you forget to add "identity" attribute to your model?'
            )

    def __as_query_set(self, as_query_set: bool, result):
        """Return QuerySet either dict depends on as_query_set option"""
        if not as_query_set:
            return result

        instances = [
            type(self._model, self._mro, {**self.__dict__, **(row or {})})()
            for row in result
        ]
        return QuerySet(self._model, self._identity, self._query, self._mro, instances)

    def count(self) -> int:
        """Return number of instances in QuerySet"""
        return len(self._instances)

    def delete(self):
        """
        Used to delete multiple instances

        Example:

        some = MyModel.manager.filter(Name='Some', as_json=False) -> QuerySet([<MyModel 1>, <MyModel 2>])
        some.delete()
        """
        if not self._instances:
            logging.warning('QuerySet is empty nothing to delete. Canceling')
            return

        model = normalize_model(self._model)
        bind = binding(self._instances)
        sql = f'DELETE FROM "{model}" WHERE "{model}"."{self._identity}" IN ({bind});'
        self._query(sql, self.__map_to_identity)

    def update(self, as_query_set: bool = False, **kwargs):
        """
        Used to update multiple instances

        Example:

        some = MyModel.manager.filter(Name='Some', as_json=False) -> QuerySet([<MyModel 1>, <MyModel 2>])
        some.update(Name='Other', as_query_set=True) -> QuerySet([<MyModel 1>, <MyModel 2>])
        either
        some.update(Name='Other') -> [{'id':1, 'Name': 'Other'}, {'id':2, 'Name': 'Other'}]
        """
        if not self._instances:
            logging.warning('QuerySet is empty nothing to update. Canceling')
            return []

        if not kwargs:
            raise ModelOperationError(
                'You should provide at least one field to update. '
                'Example .update(Name="Some")'
            )

        model = normalize_model(self._model)
        bind = binding(self._instances)
        values = ', '.join([f'"{key}" = {dump_value(value)}' for key, value in kwargs.items()])

        sql = f'UPDATE "{model}" SET {values} WHERE "{model}"."{self._identity}" IN ({bind}) RETURNING*;'

        cursor = self._query(sql, self.__map_to_identity)
        result = serializer(cursor, many=True)

        return self.__as_query_set(as_query_set, result)

    def filter(self, as_query_set: bool = True, operand='AND', operator='=', **kwargs):
        """
        Used to chain multiple select queries

        Example:
            class Users(Model):
                database = 'users'
                identity = 'user_id'

                id = Field(default=uuid.uuid4, category=str, json='id')
                email = Field(default=random_string, json='email', max_length=200, category=str)

            Users.manager.filter(id=(1, 2, 3,), operand='IN', as_json=False).filter(email='some@gmail.com')

            It will make 2 queries:
            SELECT * FROM "users" WHERE "users"."id" IN (1, 2, 3); -> for example returned 2 users
            SELECT * FROM "users" WHERE "users"."id" IN (1, 2) AND "users"."email" = some@gmail.com;
        """
        if not self._instances:
            logging.warning('QuerySet is empty nothing to update. Canceling')
            return []

        model = normalize_model(self._model)
        bind = binding(self._instances)
        sql = f'SELECT * FROM "{model}" WHERE "{model}"."{self._identity}" IN ({bind})'
        values = tuple(kwargs.values())

        if kwargs:
            sql += where(model, operand, operator, 'AND', **kwargs)

        cursor = self._query(sql, (*self.__map_to_identity, *values))
        result = serializer(cursor, many=True)
        return self.__as_query_set(as_query_set, result)
