Basic
----

Working with models can be working with objects

Let's create an object based on the model

```python
from models_manager import Model, Field


class User(Model):
    id = Field(json='id', category=int)
    username = Field(json='username', category=str)
    email = Field(json='email', category=str)


user = User(id=1, username='some', email='other')

user.id
'<Field: 1>'

user.id.value
1
```

!!! warning

    Note that `user.id` does not return an `id` value, but a 
    field object that contains data about this field

Now let's take a closer look at how we can manipulate our object.

```python hl_lines="12 13"
from models_manager import Model, Field


class User(Model):
    id = Field(json='id', category=int)
    username = Field(json='username', category=str)
    email = Field(json='email', category=str)


user = User(id=1, username='some', email='other')

user.manager.to_dict()
{'id': 1, 'username': 'some', 'email': 'other'}
```

From the example above, you can see that our object has a `manager` attribute. With which we can receive the object as a
dictionary, generate a schema, use the object to interact with the database, and so on.


List of objects
----

Now let's complicate our model and add nested objects to it.

```python
from typing import List

from models_manager import Model, Field


class Tenant(Model):
    id = Field(json='id', category=int)
    name = Field(json='name', category=str)


class User(Model):
    id = Field(json='id', category=int)
    username = Field(json='username', category=str)
    email = Field(json='email', category=str)
    tenants = Field(json='tenants', category=List[Tenant])


tenants = [Tenant(id=1, name='some'), Tenant(id=2, name='Other')]
user = User(id=1, username='some', email='other', tenants=tenants)
```

We have now added a `tenants` field to our user, which contains a list of Tenant objects. Now, when creating an object,
we specify the `tenants` parameter and pass a list with Tenant objects there

Now let's try to get the value of the `tenants` field and generate a dictionary

```python hl_lines="21 22 23 24 25 26 27 28 29 30 31 32 33"
from typing import List

from models_manager import Model, Field


class Tenant(Model):
    id = Field(json='id', category=int)
    name = Field(json='name', category=str)


class User(Model):
    id = Field(json='id', category=int)
    username = Field(json='username', category=str)
    email = Field(json='email', category=str)
    tenants = Field(json='tenants', category=List[Tenant])


tenants = [Tenant(id=1, name='some'), Tenant(id=2, name='Other')]
user = User(id=1, username='some', email='other', tenants=tenants)

user.tenants.value
'[<Model: Tenant>, <Model: Tenant>]'

user.manager.to_dict()
{
    'id': 1,
    'username': 'some',
    'email': 'other',
    'tenants': [
        {'id': 1, 'name': 'some'},
        {'id': 2, 'name': 'Other'}
    ]
}
```

From the example above, we see that inside the `Users model` there are a tenants attribute that contains a list
of `Tenant` objects. When we serialize this object using the `to_dict()` method, we get a nested object structure
