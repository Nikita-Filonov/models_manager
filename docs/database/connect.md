Connect is a class for establishing a database connection and also for interacting with the database. Each model
internally uses the `Connect` class. Connect can establish multiple connections to different databases at the same time.

Let's analyze a simple example for interacting with the database through the context manager

```python
from models_manager import Connect

with Connect(dbname='stuff', is_lazy=False) as query:
    result = query('SELECT * FROM "user"')
```

Output the result

```python hl_lines="6 7 8 9 10 11"
from models_manager import Connect

with Connect(dbname='stuff', is_lazy=False) as query:
    result = query('SELECT * FROM "user"')

    for user in result:
        print(user)

(1, 'username1', 'email1')
(2, 'username2', 'email2')
(3, 'username3', 'email3')
...
```

Result serialization

```python hl_lines="2 7 8 9 10 11 12"
from models_manager import Connect
from models_manager.utils import serializer

with Connect(dbname='stuff', is_lazy=False) as query:
    result = query('SELECT * FROM "user"')

    for user in serializer(result, many=True):
        print(user)

{'id': 1, 'username': 'username1', 'email': 'email1'}
{'id': 2, 'username': 'username2', 'email': 'email2'}
{'id': 3, 'username': 'username3', 'email': 'email3'}
...
```
