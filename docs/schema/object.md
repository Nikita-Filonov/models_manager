Let's go back to the user model and try to validate json

```json
{
  "id": 1,
  "username": "some",
  "email": "other"
}
```

Let's describe our model

```python
from models_manager import Model, Field


class User(Model):
    id = Field(default=1, json='id', category=int)
    username = Field(default='some', json='username', category=str)
    email = Field(default='other', json='email', category=str)
```

We described the model where we indicated the categories for each field

!!! note

    You can read more about categories and other 
    field arguments [here](../field.md)

Now let's generate a schema that will describe how the json of our model should look like.

```python hl_lines="10 11 12 13 14 15 16 17 18 19 20"
from models_manager import Model, Field


class User(Model):
    id = Field(default=1, json='id', category=int)
    username = Field(default='some', json='username', category=str)
    email = Field(default='other', json='email', category=str)


User.manager.to_schema

{
    'type': 'object',
    'properties': {
        'id': {'type': 'number'},
        'username': {'type': 'string'},
        'email': {'type': 'string'}
    },
    'required': ['id', 'username', 'email']
}
```

From here we see that:

- id - number
- username - string
- email - string

Max length
---

Let's add more specifics for some fields

```python hl_lines="6 7 16 17 18 19 20 21 22 23 24 25"
from models_manager import Model, Field


class User(Model):
    id = Field(default=1, json='id', category=int)
    username = Field(default='some', json='username', category=str, max_length=100)
    email = Field(default='other', json='email', category=str, max_length=70)


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
        }
    },
    'required': ['id', 'username', 'email']
}
```

Now we can see that the username is in a certain length range from 0 to 100, just like the email field

Required
---

Now let's see how we can validate optional fields in an object. Imagine now that the user object has an optional `token`
field, which may or may not be

```json
{
  "id": 1,
  "username": "some",
  "email": "other"
}
```

Also valid

```json hl_lines="5"
{
  "id": 1,
  "username": "some",
  "email": "other",
  "token": "some-token"
}
```

Let's add a new token field to our user model

```python hl_lines="8 17 19"
from models_manager import Model, Field


class User(Model):
    id = Field(default=1, json='id', category=int)
    username = Field(default='some', json='username', category=str)
    email = Field(default='other', json='email', category=str)
    token = Field(default='some-token', json='token', is_related=True)


{
    'type': 'object',
    'properties': {
        'id': {'type': 'number'},
        'username': {'type': 'string'},
        'email': {'type': 'string'},
        'token': {'type': ['string', 'null']}
    },
    'required': ['id', 'username', 'email']
}
```

!!! note

    Notice that we have added the `is_related` argument 
    to the `token` field. You can read more about field 
    arguments [here](../field.md)
    
