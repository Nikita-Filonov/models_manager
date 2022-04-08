Currently, only PostgreSQL is supported. If you need a custom manager for the database, then you can inherit from the
ModelManager and override the necessary methods for the database.

Let's prepare our project to interact with the database

1. The first thing we need to do is add settings. In your settings.py or any other settings file, import the database
   manager settings
   ```python
   import models_manager.settings
   ```

2. Now we will specify the credentials for connecting to the database
   ```python hl_lines="1 5 6 7 8 9 10"
   import os

   import models_manager.settings

   models_manager.settings.DATABASE = {
      'host': os.environ.get('DB_HOST', 'some.db.host'),
      'port': os.environ.get('DB_POST', 5432),
      'user': os.environ.get('DB_USER', 'user'),
      'password': os.environ.get('DB_PASSWORD', 'password'),
   }
   ```

3. Next, we need to point to the database or databases, if we have more than one, to which we want to connect.
   ```python hl_lines="12"
   import os

   import models_manager.settings

   models_manager.settings.DATABASE = {
      'host': os.environ.get('HOST', 'some.db.host'),
      'port': os.environ.get('POST', 5432),
      'user': os.environ.get('USER', 'user'),
      'password': os.environ.get('PASSWORD', 'password'),
   }

   models_manager.settings.DATABASES = ['projects', 'stuff', 'common']
   ```

4. Optional setting for outputting a query to the database
   ```python hl_lines="14"
   import os

   import models_manager.settings

   models_manager.settings.DATABASE = {
      'host': os.environ.get('HOST', 'some.db.host'),
      'port': os.environ.get('POST', 5432),
      'user': os.environ.get('USER', 'user'),
      'password': os.environ.get('PASSWORD', 'password'),
   }

   models_manager.settings.DATABASES = ['projects', 'stuff', 'common']

   models_manager.settings.DATABASE_LOGGING = True
   ```

5. Now in our model, through which we want to interact with the database, we need to add arguments `identity`
   , `database`
   ```python hl_lines="5 6"
   from models_manager import Model, Field


   class User(Model):
      identity = 'user_id'
      database = 'stuff'

      user_id = Field(json='id')
      username = Field(json='username')
   ```

    - `identity` - Used to specify the table ID, usually the primary key
    - `database` - The name of the database in which this model resides. This will give the manager an idea which
      database connection to use to execute the query.

That's all, now you can use the model you need to interact with the database
