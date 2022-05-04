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


Dictionary with object
----

Now let's look at an example in which we will have a dictionary with an object inside

```python
from typing import Dict

from models_manager import Model, Field


class Tenant(Model):
    id = Field(json='id', category=int)
    name = Field(json='name', category=str)


class User(Model):
    id = Field(json='id', category=int)
    username = Field(json='username', category=str)
    email = Field(json='email', category=str)
    tenant_ref = Field(json='tenantRef', category=Dict[str, Tenant])


tenant_ref = {'some': Tenant(id=1, name='some')}
user = User(id=1, username='some', email='other', tenantRef=tenant_ref)
```

Now we have added the `tenant_ref` field, which is a dictionary, and inside this dictionary we have a Tenant object.
Let's generate a dictionary based on the `User` model and look at the value of the `tenant_ref` field

!!! warning

    Notice that when we created the `User` object, we specified the `tenantRef` attribute, 
    not the `tenant_ref` attribute. 
    When generating a model object, the names of the attributes are passed in the form in which they appear 
    in the json representation

```python hl_lines="21 22 23 24 25 26 27 28 29 30 31 32 33"
from typing import Dict

from models_manager import Model, Field


class Tenant(Model):
    id = Field(json='id', category=int)
    name = Field(json='name', category=str)


class User(Model):
    id = Field(json='id', category=int)
    username = Field(json='username', category=str)
    email = Field(json='email', category=str)
    tenant_ref = Field(json='tenantRef', category=Dict[str, Tenant])


tenant_ref = {'some': Tenant(id=1, name='some')}
user = User(id=1, username='some', email='other', tenantRef=tenant_ref)

user.tenant_ref.value
"{'some': <Model: Tenant>}"

user.manager.to_dict()
{
    'id': 1,
    'username': 'some',
    'email': 'other',
    'tenantRef': {
        'some': {'id': 1, 'name': 'some'}
    }
}
```

From the example above, we can see that the dictionary with the object was serialized when the `to_dict()` method was
called.
