We can generate json schema to validate json objects. The schema is generated dynamically based on the model.

This allows us to control the objects that our API returns to us. In case of non-compliance with the scheme, find bugs
and errors

Suppose we have an API that returns json

```json
{
  "id": 1,
  "username": "some",
  "email": "other"
}
```

Let's describe the model that will describe the returned json and validate it

```python
from jsonschema import validate

from models_manager import Model, Field


class User(Model):
    id = Field(default=1, json='id', category=int)
    username = Field(default='some', json='username', category=str, max_length=100)
    email = Field(default='other', json='email', category=str, max_length=70)


user_json = get_user().json()
schema = User.manager.to_schema

validate(instance=user_json, schema=schema)
```

Exclude schema
---

If you want to dynamically exclude fields from the json schema, then there is the `exclude_schema` parameter for this.
As values, a list of fields is passed as strings or Field objects

```python
from models_manager import Model, Field


class User(Model):
    id = Field(json='id', category=int, default=1)
    email = Field(json='email', category=str, max_length=100)
    username = Field(json='username', category=str, max_length=50)


user = User(exclude_schema=[User.id, User.email])
user.manager.to_schema
{
    'title': 'User',
    'type': 'object',
    'properties': {
        'username': {'maxLength': 50, 'type': 'string'}
    },
    'required': ['username']
}
```
