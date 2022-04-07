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
insert it into the database

```python
str, int, float, list, dict, bool, Callable, None
```

Example with callable object

```python
from models_manager import Field

func = lambda: []

items = Field(default=func)
items.get_default

"[{'key': 'value'}]"
```

!!! warning

    Note that the `"[{'key': 'value'}]"` object is a string. 
    This happens because we did not pass the category

Callable object and category together

```python
from models_manager import Field

func = lambda: []

items = Field(default=func, category=list)
items.get_default

[{'key': 'value'}]
```

!!! note

    Now we get the value as a list

json
---

value
---

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

