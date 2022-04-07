Let's imagine that our user can belong to several tenants at once

```json
{
  "id": 1,
  "username": "some",
  "email": "other",
  "tenant": [
    {
      "id": "some1",
      "name": "Customer1"
    },
    {
      "id": "some2",
      "name": "Customer2"
    }
  ]
}
```

Let's make a model that can validate a list of tenants

```python hl_lines="19"
from models_manager import Model, Field


class Tenant(Model):
    id = Field(default='some', json='id')
    name = Field(default='Customer', json='name')


tenant = {
    "id": "some",
    "name": "Customer"
}


class User(Model):
    id = Field(default=1, json='id', category=int)
    username = Field(default='some', json='username', category=str)
    email = Field(default='other', json='email', category=str)
    tenant = Field(default=tenant, json='tenant', category=list, related_to=Tenant)
```

!!! note

    Note that now, unlike validating just an object, 
    we specify the list category, this tells our model 
    that tenant is a list of objects

Now let's generate a schema for the nested list of objects

```python hl_lines="22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42"
from models_manager import Model, Field


class Tenant(Model):
    id = Field(default='some', json='id')
    name = Field(default='Customer', json='name')


tenant = {
    "id": "some",
    "name": "Customer"
}


class User(Model):
    id = Field(default=1, json='id', category=int)
    username = Field(default='some', json='username', category=str)
    email = Field(default='other', json='email', category=str)
    tenant = Field(default=tenant, json='tenant', category=list, related_to=Tenant)


User.manager.to_schema
{
    'type': 'object',
    'properties': {
        'id': {'type': 'number'},
        'username': {'type': 'string'},
        'email': {'type': 'string'},
        'tenant': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'string'},
                    'name': {'type': 'string'}
                },
                'required': ['id', 'name']
            }
        }
    },
    'required': ['id', 'username', 'email', 'tenant']
}
```
