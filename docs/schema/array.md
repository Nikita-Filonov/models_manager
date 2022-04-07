Let's analyze an example where we get a list of user objects

```json
[
  {
    "id": 1,
    "username": "some1",
    "email": "other1"
  },
  {
    "id": 2,
    "username": "some2",
    "email": "other2"
  },
  {
    "id": 3,
    "username": "some3",
    "email": "other3"
  }
]
```

We can use the same model we did to validate just the user object

```python
from models_manager import Model, Field


class User(Model):
    id = Field(default=1, json='id', category=int)
    username = Field(default='some', json='username', category=str)
    email = Field(default='other', json='email', category=str)
```

Now we generate a schema for validating the list of objects

```python hl_lines="10 11 12 13 14 15 16 17 18 19 20 21 22"
from models_manager import Model, Field


class User(Model):
    id = Field(default=1, json='id', category=int)
    username = Field(default='some', json='username', category=str)
    email = Field(default='other', json='email', category=str)


User.manager.to_array_schema
{
    'type': 'array',
    'items': {
        'type': 'object',
        'properties': {
            'id': {'type': 'number'},
            'username': {'type': 'string'},
            'email': {'type': 'string'}
        },
        'required': ['id', 'username', 'email']
    }
}
```


