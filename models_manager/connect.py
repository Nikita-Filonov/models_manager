import logging
from typing import Optional

import psycopg2
from psycopg2 import OperationalError

from models_manager.manager.exeptions import DatabaseNameError
from models_manager.utils import retry

logging.basicConfig(level=logging.INFO)


class QueryManager:
    """
    Wrapper over for executing query
    """

    def __init__(self, connection, cursor):
        self._connection = connection
        self._cursor = cursor

    def query(self, query, args=()):
        """
        Wrapper along 'execute' method. Should be used
        to execute sql queries.

        This method also has included logger, so we can see executed queries.
        To turn off logging queries, change DATABASE_LOGGING to False, in settings.py
        """
        from models_manager.settings import DATABASE_LOGGING
        if DATABASE_LOGGING:
            logging.info(query % args if isinstance(args, tuple) else tuple(args))

        try:
            self._cursor.execute(query, args)
        except Exception as error:
            self._connection.rollback()
            logging.error(error)
        else:
            self._connection.commit()

        return self._cursor


class Connect:
    """
    The main task of this class is to manage connections
    to databases of various services.

    We have multiple services that uses different databases,
    currently psycopg2 does not have api to switch between
    databases dynamically. So we have to manage that our self.

    Example:

    - As context:
      with Connect('users') as query:
           query('SELECT * FROM "Users"')

    - As normal function:
      query = Connect().users
      query('SELECT * FROM "Users"')

    In examples above "users" can be any attr, it depends on the
    database name, so if you pass dbname='some', then usage will be like:

    users = Connect().some
    some('SELECT * FROM "Users"')
    """

    def __init__(self, dbname=None, is_lazy=True):
        self.__context_dbname = dbname

        if not is_lazy:
            self._setup_connections(dbname)

    def __getattr__(self, item):
        if not self.__dict__.get('_connections'):
            self._setup_connections()

        connection = self._connections[item]
        cursor = self._cursors[item]
        return QueryManager(connection, cursor).query

    def __enter__(self):
        try:
            connection = self._connections[self.__context_dbname]
            cursor = self._cursors[self.__context_dbname]
            return QueryManager(connection, cursor).query
        except KeyError:
            raise DatabaseNameError('To use query in context manager provide "dbname"')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connections[self.__context_dbname].close()
        self._cursors[self.__context_dbname].close()

    @retry(times=10, exceptions=(OperationalError,))
    def _setup_connections(self, dbname: Optional[str] = None):
        """Setting up connections to multiple databases"""
        from models_manager.settings import DATABASES, DATABASE
        databases = DATABASES if dbname is None else [dbname]
        self._connections = {db: psycopg2.connect(**{**DATABASE, 'dbname': db}) for db in databases}
        self._cursors = {db: conn.cursor() for conn, db in zip(self._connections.values(), databases)}
