Continuing with the user model example, let's imagine that we need to extend this model

```python
from models_manager import Model, Field


class User(Model):
    id = Field(default=1, json='id')
    username = Field(default='some', json='username')
    email = Field(default='other', json='email')
```

So now we have new "User" object

```json hl_lines="5 6 7 8 9"
{
  "id": 1,
  "username": "some",
  "email": "other",
  "token": "some-token",
  "tenant": {
    "id": 1,
    "name": "Customer"
  }
}
```

Let's upgrade our "User" model

```python hl_lines="10 11 12 13 14 15 16 17 18"
from models_manager import Model, Field


class User(Model):
    id = Field(default=1, json='id')
    username = Field(default='some', json='username')
    email = Field(default='other', json='email')


tenant = {
    "id": 1,
    "name": "Customer"
}


class CustomerUser(User):
    token = Field(default='some-token', json='token')
    tenant = Field(default=tenant, json='tenant')
```

So now we can get "User" and "CustomerUser" objects json without duplicating same fields

```python hl_lines="20 21 22 23 24 25 26 27 28 29 30 31"
from models_manager import Model, Field


class User(Model):
    id = Field(default=1, json='id')
    username = Field(default='some', json='username')
    email = Field(default='other', json='email')


tenant = {
    "id": 1,
    "name": "Customer"
}


class CustomerUser(User):
    token = Field(default='some-token', json='token')
    tenant = Field(default=tenant, json='tenant')
    
CustomerUser.manager.to_json

{
  "id": 1,
  "username": "some",
  "email": "other",
  "token": "some-token",
  "tenant": {
    "id": 1,
    "name": "Customer"
  }
}
```

---
For example, we need to override some field with new value

```json hl_lines="3"
{
  "id": 1,
  "username": "another",
  "email": "other"
}
```

Let's do this

```python hl_lines="14 15 16 17 18 19 20"
from models_manager import Model, Field


class User(Model):
    id = Field(default=1, json='id')
    username = Field(default='some', json='username')
    email = Field(default='other', json='email')


class SpecialUser(User):
    username = Field(default='another', json='username')


SpecialUser.manager.to_json

{
    "id": 1,
    "username": "another",
    "email": "other"
}
```

This way we can overwrite the attributes of the parent model
