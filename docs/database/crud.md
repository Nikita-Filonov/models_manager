Let's create a simple table and use it as an example to analyze the operations of reading, creating, updating, deleting

Our "user" database table

| id  | username | email |
| :---| :------- | :---- |
| 1   | some1    | email1 |
| 2   | some2    | email2 |
| 3   | some3    | email3 |

Our python model

```python
from models_manager import Model, Field
from models_manager.utils import random_number, random_string


class User(Model):
    identity = 'users'
    database = 'stuff'

    id = Field(default=random_number, category=int)
    username = Field(default=random_string, category=str)
    email = Field(default=random_string, category=str)

    def __str__(self):
        return f'<User: {self.id}>'
```

### **Get**

Get always returns a single object. If the requested object is not in the database, it will raise an error

```python
User.manager.get(id=1)  # returns python dict
{
    'id': 1,
    'username': 'some1',
    'email': 'email1'
}

User.manager.get(id=1, as_json=False)  # returns user object
'<User: 1>'

User.manager.get(id=100)  # user with id 100 does not exists
"ModelDoesNotExists: 'User' with {'id': 100} does not exists"
```

### **Filter**

Filter returns a list of objects. If the objects are not found in the database, it will return an empty list

```python
User.manager.filter(id=1)  # returns python list of dicts
[
    {
        'id': 1,
        'username': 'some1',
        'email': 'email1'
    }
]

User.manager.filter(id__in=(1, 2), as_json=False)  # returns list of user objects
['<User: 1>', '<User: 2>']

# no such users in our database, filter will return empty list
User.manager.filter(id__in=(100, 200))
[]
```

### **Create**

Creates an object and returns the created object. Values for creation are taken from the fields of the model

```python
User.manager.create()  # create user with some random values
{
    'id': 9,
    'username': 'pF8i78S0ncdatjR5UDYE6uMDg5yxEwLk',
    'email': 'i7KbUPGrNGBr5yW9mu6lD6JPMxX3FnKCaTQlSuwR9fLM'
}

# override username with custom value, instead of random
User.manager.create(username='custom')
{
    'id': 32,
    'username': 'custom',
    'email': 'BzpzI8cc54ztqJLCgo7gUCYe8BhGzZxgt7c63l'
}

User.manager.create(id=100, as_json=False)  # returns user object
'<User: 100>'
```

### **Update**

Allows you to update the object. Returns the updated object

```python
user = User.manager.get(id=1, as_json=False)
user = user.manager.update(username='new_username', as_json=False)

user  # returns user object
'<User: 1>'

user.username  # updated username value
'new_username'
```

### **Delete**

Removes an object from the database. Returns nothing

```python
user = User.manager.get(id=1, as_json=False)
user.manager.delete()  # deleting user object with id=1
```

### **Is exists**

Return a boolean, True if the entities are present in the database, False if the entities are not in the database.
Recommended to use to check the presence of an entity in the database

```python
is_user_exists = User.manager.is_exists(id=1)

is_user_exists  # user with id=1 exists, True
True

is_user_exists = User.manager.is_exists(id=100)

is_user_exists  # user with id=100 does not exists, False
False
```

