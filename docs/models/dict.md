Generating dynamic json object based on model. This is one of the most powerful feature of using models

Generating json based on model
---
---

Let's imagine that we have a user object, and we need to get this object with random values each time

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "username": "some random username",
  "email": "some random email"
}
```

So let's create a model which will generate us json above

!!! note

    Id should be dynamic value. Usually when we write auto tests, 
    we use dynamic values. Just like our API can't always 
    accept static values, and vice versa they must be unique 
    each time

```python
import uuid

from models_manager import Model, Field
from models_manager.utils import random_string


class User(Model):
    id = Field(default=uuid.uuid4, json='id', category=str)
    username = Field(default=random_string, json='username', category=str)
    email = Field(default=random_string, json='email', category=str)
```

Let's see what's going on here

```python
import uuid

from models_manager.utils import random_string

callable(uuid.uuid4)  # True
callable(random_string)  # True

callable(uuid.uuid4())  # False 
callable(random_string())  # False 
```

In this case, uuid4, random_string are callable objects. When generating json, these objects will be called and return
values will be obtained from them

Let's try to use our user model and generate random json

```python hl_lines="13 20"
import uuid

from models_manager import Model, Field
from models_manager.utils import random_string


class User(Model):
    id = Field(default=uuid.uuid4, json='id', category=str)
    username = Field(default=random_string, json='username', category=str)
    email = Field(default=random_string, json='email', category=str)


User.manager.to_dict()
{
    'id': '992ae8a2-ab6d-4d16-a7fd-e009bdcbff4c',
    'username': 'P8aNC414bqfSZEyUVpgZZQt',
    'email': 'UDxG3bKhvlLuM8n1LFCtfbZqwlKihogkL6BM8gfVIVk28'
}

User.manager.to_dict()
{
    'id': 'b3a02f98-7691-4a30-a42d-a1a3c600b584',
    'username': 'XUzl4QLP5mENis0tadeqacSSHf0vwaySeGQgV7S64R2M',
    'email': 'h1OnsjE5s1UXwTeEpuB5GbPPLF8'
}
```

Now we get random json values every time we call the `to_dict()` method


Json key
---

The `json_key` argument is used to control the keys that will be used when serializing the object into a dictionary

Consider an example where the field names differ from their names in json view

```python
from typing import Optional

from models_manager import Model, Field


class User(Model):
    id = Field(json='Id', category=Optional[str])
    username = Field(json='Username', category=Optional[str])


User.manager.to_dict(json_key=False)
{'id': None, 'username': None}

User.manager.to_dict(json_key=True)
{'Id': None, 'Username': None}
```

From the example above, we see that if `json_key=True`, then we get a dictionary with json keys, otherwise we get the
original field names


Exclude
---

To exclude fields that will be in the model dictionary, you can use the `exclude` parameter. The arguments are a list of
Field objects or a list of fields as strings

```python
from models_manager import Model, Field


class User(Model):
    id = Field(json='id', category=int, default=1)
    username = Field(json='username', category=str, default='some')


User.manager.to_dict(exclude=[User.id])
{'username': 'some'}

User.manager.to_dict(exclude=['id'])
{'username': 'some'}
```

Now we can see that the `id` field has been excluded from the model dictionary

You can also exclude fields when creating an object

```python
from models_manager import Model, Field


class User(Model):
    id = Field(json='id', category=int, default=1)
    username = Field(json='username', category=str, default='some')


user = User(exclude_dict=[User.id])
user.manager.to_dict()
{'username': 'some'}

user = User(exclude_dict=['id'])
user.manager.to_dict()
{'username': 'some'}
```

If you specify the fields to be excluded as strings, then you must specify their format in `json`
