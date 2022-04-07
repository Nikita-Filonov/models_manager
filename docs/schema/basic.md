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
from models_manager import Model, Field


class User(Model):
    id = Field(default=1, json='id', category=int)
    username = Field(default='some', json='username', category=str, max_length=100)
    email = Field(default='other', json='email', category=str, max_length=70)


user_json = get_user().json()
schema = User.manager.to_schema

validate_json(json=user_json, schema=schema)
```
