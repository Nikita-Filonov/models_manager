Now let's imagine that our user has a role field that can only have a certain set of values.

According to business logic, our user can have the roles of `junior`, `middle`, `senior`, `expert`

```json
{
  "id": 1,
  "username": "some",
  "email": "other",
  "role": "junior"
}
```

Let's describe it in terms of a python object

```python
from enum import Enum


class Roles(Enum):
    JUNIOR = 'junior'
    MIDDLE = 'middle'
    SENIOR = 'senior'
    EXPERT = 'expert'
```

Now let's create a model. Let's describe the role field and indicate that the role field can only have a certain range
of values

```python hl_lines="1 4 11 11 12 13 14 15"
from models_manager import Model, Field, FieldGenericEnum


class Roles(FieldGenericEnum):
    JUNIOR = 'junior'
    MIDDLE = 'middle'
    SENIOR = 'senior'
    EXPERT = 'expert'


class User(Model):
    id = Field(default=1, json='id', category=int)
    username = Field(default='some', json='username', category=str)
    email = Field(default='other', json='email', category=str)
    role = Field(default=Roles.JUNIOR.value, json='role', category=str, choices=Roles.to_list())
```

!!! note

    We have added a `role` field to our user model. 
    Notice the choices argument.
    You can read more about field arguments [here](../field.md)

`Roles.to_list()` will return us a list of the available roles. We pass this list as the choices argument inside
the `role` field

```python
from models_manager import FieldGenericEnum


class Roles(FieldGenericEnum):
    JUNIOR = 'junior'
    MIDDLE = 'middle'
    SENIOR = 'senior'
    EXPERT = 'expert'


Roles.to_list()
['junior', 'middle', 'senior', 'expert']
```

Now we have described the model and the list of available roles. Let's generate a schema

```python hl_lines="26 27 28 29"
from models_manager import Model, Field, FieldGenericEnum


class Roles(FieldGenericEnum):
    JUNIOR = 'junior'
    MIDDLE = 'middle'
    SENIOR = 'senior'
    EXPERT = 'expert'


class User(Model):
    id = Field(default=1, json='id', category=int)
    username = Field(default='some', json='username', category=str)
    email = Field(default='other', json='email', category=str)
    role = Field(default=Roles.JUNIOR.value, json='role', category=str, choices=Roles.to_list())


User.manager.to_schema

{
    'type': 'object',
    'properties': {
        'id': {'type': 'number'},
        'username': {'type': 'string'},
        'email': {'type': 'string'},
        'role': {
            'type': 'string',
            'enum': ['junior', 'middle', 'senior', 'expert']
        }
    },
    'required': ['id', 'username', 'email', 'role']
}
```

Now we see that role is not just a string, but a string that can only be represented by a certain set of values.

This means that if, for example, our API returns to us some invalid choice, for example

```json
{
  "id": 1,
  "username": "some",
  "email": "other",
  "role": "some error instead of role"
}
```

Then our test will detect this error and fail
