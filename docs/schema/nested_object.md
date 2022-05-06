!!! warning

    The `related_to` attrivute is deprecated. Use typing
    annotation on category attribute. 
    Read more [with_models](./with_models.md), [advanced](./advanced.md)

But we still have a tenant field which is of type object and this is not informative because object can be any json.

```json
{
  "id": 1,
  "username": "some",
  "email": "other",
  "tenant": {
    "id": "some",
    "name": "Customer"
  }
}
```

Let's describe the tenant object as a model

```python
from models_manager import Model, Field


class Tenant(Model):
    id = Field(default='some', json='id')
    name = Field(default='Customer', json='name')
```

Now let's put everything together and generate a schema for nested json with tenant

```python hl_lines="4 5 6 19 38 39 40 41 42 43 44 45"
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
    username = Field(default='some', json='username', category=str, max_length=100)
    email = Field(default='other', json='email', category=str, max_length=70)
    tenant = Field(default=tenant, json='tenant', category=dict, related_to=Tenant)


User.manager.to_schema

{
    'type': 'object',
    'properties': {
        'id': {'type': 'number'},
        'username': {
            'type': 'string',
            'minLength': 0,
            'maxLength': 100
        },
        'email': {
            'type': 'string',
            'minLength': 0,
            'maxLength': 70
        },
        'tenant': {
            'type': 'object',
            'properties': {
                'id': {'type': 'string'},
                'name': {'type': 'string'}
            },
            'required': ['id', 'name']
        }
    },
    'required': ['id', 'username', 'email', 'tenant']
}
```

Now we see that tenant is not just an abstract object, but a concrete object with certain fields.

!!! note

    Pay attention to the `related_to` attribute to which we passed the 
    `Tenant` model object. 
    You can read more about field arguments [here](../field.md)
