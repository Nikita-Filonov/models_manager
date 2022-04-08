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

choices
---

related_to
---

only_json
---

is_related
---

max_length
---

