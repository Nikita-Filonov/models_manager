Used to build filters based on binary operators. Helps build more complex database queries

Consider the use of logical operators on the example of the user model

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

### OR

`|` - Bitwise OR

```python
from models_manager import Q

User.manager.filter(Q(id__in=(1, 2)) | Q(username='some'))
```

### AND

`&` - Bitwise AND

```python
from models_manager import Q

User.manager.filter(Q(id__in=(1, 2)) & Q(username='some'))
```

### OR + AND

```python
from models_manager import Q

User.manager.filter(
    (Q(id__in=(1, 2)) & Q(username='some')) |
    (Q(id__lt=100) & Q(username__like='other'))
)
```

Above were an example of how you can build logical expressions for database queries
