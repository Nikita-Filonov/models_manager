# Models Manager

Library for creating object models and for interacting with the database. Provides simple interface for that. For
databases only PostgreSQL supported from the box.

For databases enabled support for multiple connections

### Simple example:

```python
from models_manager.manager.field import Field
from models_manager.manager.model import Model


class User(Model):
    email = Field(default='some@gmail.com', json='email', max_length=255)
    username = Field(default='some', json='username', null=True, max_length=255)
    password = Field(default='other', json='password', max_length=255)


json = User.manager.to_json
print(json)

json_negative = User.manager.to_negative_json()
print(json_negative)

user_schema = User.manager.to_schema
print(user_schema)

user_array_schema = User.manager.to_array_schema
print(user_array_schema)  
```

### Working with databases:

To work with database, we have to define settings. So, somewhere in your
`settings.py`:

```python
import models_manager.settings

models_manager.settings.DATABASE = {
    'host': 'some',
    'port': 5432,
    'user': 'user',
    'password': 'password',
}

models_manager.settings.DATABASES = ['some', 'other', 'another']
models_manager.settings.DATABASE_LOGGING = True
```

Then in your model you have to override `database` and `identity` attributes

```python
from models_manager.manager.field import Field
from models_manager.manager.model import Model


class User(Model):
    database = 'some'
    identity = 'id'
    
    id = Field(default=1, json='id', category=int)
    email = Field(default='some@gmail.com', json='email', max_length=255)
    username = Field(default='some', json='username', null=True, max_length=255)
    password = Field(default='other', json='password', max_length=255)
```
