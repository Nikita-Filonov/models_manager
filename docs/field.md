Field is an object that describes a model field

category
---

Category argument, which is responsible for the field value type. The following categories are supported:

| Type          | Description                          | Schema |
| :-------------| :----------------------------------- | :----- |
| `int`         | Integer numbers `1`, `2`, `3`, `4`  | number |
| `float`       | Float numbers `1.5`, `2.6`, `7.8` | number |
| `str`         | Strings `"some"`, `"other"` | string |
| `bool`        | Boolean `True/False` | boolean |
| `list`        | List of dicts/strings/integers `[1, 2, 3]`, `["1", "2", "3"]` | array |
| `tuple`       | Tuple of dicts/strings/integers `(1, 2, 3)`, `("1", "2", "3")` | array |
| `dict`        | Dict `{"key": "value"}` | object |
| `None`        | `None` | null |

Let's take a simple example

```python
from models_manager import Model, Field


class User(Model):
    username = Field(default=1, json='username', category=str)
    email = Field(default=2, json='email', category=int)


User.manager.to_json
{
    'username': '1',
    'email': 2
}
```

default
---
Default field value. Can be any of supported objects. Provides a default value that will be used to generate json and
insert it into the database. By default `default` argument equal to `None`

```python
str, int, float, list, dict, bool, Callable, None
```

### **Basic**

Let's look at a simple example with a default value

```python
from models_manager import Field

items = Field(default=12345)

items.get_default
"12345"
```

!!! warning

    Note that the `"12345"` object is a string. 
    This happens because we did not pass the category. 
    And by default string category is used

Let's add a category to our field

```python
from models_manager import Field

items = Field(default=12345, category=int)

items.get_default
12345
```

!!! note

    Now we get the value as a integer

### **Callable**

Example with callable object

```python
from models_manager import Field


def get_items_from_api():
    """Some function which will get items from API"""
    return get_items().json()


items = Field(default=get_items_from_api, category=list)
items.get_default

[
    {'key': 'value1'},
    {'key': 'value2'},
    {'key': 'value3'}
]
```

Let's explain what's going on here. The `get_items_from_api` function gets a list of items and this function is callable
object . This function is calling when we call the `get_default` method


json
---
The `json` argument is responsible for how the field in json will be named. Json argument is using when generating json
and schema. Let's take a simple example.

Imagine we have a user object

```json
{
  "id": 1,
  "firstName": "some",
  "lastName": "other"
}
```

Let's create a model that will describe the user object above.

```python
from models_manager import Field, Model


class User(Model):
    id = Field(json='id')
    first_name = Field(json='firstName')
    last_name = Field(json='lastName')


User.manager.to_json
{
    'id': None,
    'firstName': None,
    'lastName': None
}
```

!!! note

    Pay attention to how the model fields are naming in 
    the class and in json. The naming is different, because, 
    as a rule, the front end requires fields named in the 
    javascript style, but we work with Python code and the 
    javascript style is not suitable

```python
from models_manager import Field, Model


class GoodUser(Model):
    first_name = Field(json='firstName')  # good


class BadUser(Model):
    firstName = Field(json='firstName')  # very bad
```

value
---
The `value` argument that is responsible for the current value of the field. Unlike the default, `value` can change.
Let's take an example of using value

```python
from models_manager import Field

username = Field(default='some')
username.value = 'new value'

username.get_default
'some'
username.value
'new value'
```

As we can see, the default value does not change, unlike value, which we can change and save the current state of the
field into it. Now let's look at a more complex example with a model

```python
from models_manager import Model, Field


class User(Model):
    id = Field(default=1, json='id', category=int)
    username = Field(default='some', json='username')


new_user = User(id=2, username='other')
new_user.username.value  # username has new value
'other'
new_user.manager.to_json  # json of new_user object
{
    'id': 2,
    'username': 'other'
}

User.manager.to_json  # json with default values
{
    'id': 1,
    'username': 'some'
}
```

From the example above, `new_user` is already a new object that has its own attributes. This object can be used as an
annotation. Also, the `new_user` object contains the new `id`, `username` values that we passed when initializing the
object.

null
---

The `null` argument controls whether the field can be null - essentially empty. For example, if we specify that the
field is `null=True`, then this will affect the schema generation. Let's take a simple example

```python
from models_manager import Field

username = Field(category=str, json='username', null=True)
username.get_schema
{
    'type': ['string', 'null']
}
```

It can be seen from the example above that if we add the `null=True` argument to the field. Then when generating the
schema, we will get the variability of the field values `string` or `null`

choices
---

The `choices` argument is responsible for the variability of field values. for example, if the field has only a certain
range of values. Let's look at an example

```python
from models_manager import Model, Field, FieldGenericEnum


class ProjectStates(FieldGenericEnum):
    """This is some states of the project"""
    STARTING = 1
    PENDING = 2
    STARTED = 3
    CLOSED = 4
    STOPPED = 5


class Project(Model):
    title = Field(json='title', category=str)
    state = Field(json='state', choices=ProjectStates.to_list(), category=int)
```

Now, when creating an object or generating a schema, it will validate that the `state` field has a certain set of
values. Let's look at an example of creating an object

```python hl_lines="18 19 20 21 22 23 24 25 26"
from models_manager import Model, Field, FieldGenericEnum


class ProjectStates(FieldGenericEnum):
    """This is some states of the project"""
    STARTING = 1
    PENDING = 2
    STARTED = 3
    CLOSED = 4
    STOPPED = 5


class Project(Model):
    title = Field(json='title', category=str)
    state = Field(json='state', choices=ProjectStates.to_list(), category=int)


project_json = get_project(id=1).json()
{
    "title": "some",
    "state": 7
}

Project(**project_json)  # will raise an exception, because 7 is not valid state

'FieldException: The "state" field must be one of the 1, 2, 3, 4, 5, but 6 was received'
```

related_to
---
The `related_to` attribute is using to describe nested entities. For example, if json has a complex nested structure,
then we can describe it using this attribute. Let's imagine that we have an API that returns an object with multiple
nesting.

```json
{
  "id": 1,
  "username": "some",
  "email": "other",
  "tenant": {
    "id": 1,
    "name": "Customer"
  },
  "roles": [
    {
      "id": 1,
      "name": "Junior",
      "permissions": [
        {
          "id": 1,
          "action": "Read"
        }
      ]
    },
    {
      "id": 2,
      "name": "Middle",
      "permissions": [
        {
          "id": 1,
          "action": "Read"
        },
        {
          "id": 2,
          "action": "Create"
        }
      ]
    }
  ]
}
```

Let's describe this json object in the form of models

```python
from models_manager import Model, Field


class Tenant(Model):
    id = Field(json='id', category=int)
    name = Field(json='name', category=str)


class Permission(Model):
    id = Field(json='id', category=int)
    action = Field(json='action', category=str)


class Role(Model):
    id = Field(json='id', category=int)
    name = Field(json='name', category=str)
    permissions = Field(json='permissions', related_to=Permission, category=list)


class User(Model):
    id = Field(json='id', category=int)
    username = Field(json='username', category=str)
    email = Field(json='email', category=str)
    tenant = Field(json='tenant', category=dict, related_to=Tenant)
    roles = Field(json='roles', category=list, related_to=Role)
```

only_json
---

The `only_json` argument is using for the database. For example, if we have a field that is displayed in the json
object, but it is not in the database. For example, consider a json object and a table in a database

```json
{
  "id": 1,
  "username": "some",
  "token": "some-token which is not in database"
}
```

| id  | username |
| :---| :------- |
| 1   | some1    |
| 2   | some2    |
| 3   | some3    |

As we can see, the token field is not storing in the database, it can be dynamically calculated or cached

```python
from models_manager import Model, Field


class UserWithToken(Model):
    id = Field(json='id', category=int)
    username = Field(json='username', category=str)
    token = Field(json='token', only_json=True, category=str)
```

We described the model and specified `only_json=True` in the token field, now for any operation to the database,
the `token` field will not be used

is_related
---

max_length
---

