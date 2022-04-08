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

    id = Field(default=random_number)
    username = Field(default=random_string)
    email = Field(default=random_string)

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

### **Update**

### **Delete**

### **Is exists**
