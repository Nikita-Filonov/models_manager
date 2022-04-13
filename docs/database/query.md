### Q - query node

Used to build filters based on binary operators. Helps build more complex database queries

`Q` is a class that allows us to make complex database queries. For example, if we need to make a logical query with the
operators "and", "or" or even combine several operators at once. By itself, `Q` is not intended to be used like regular
classes. This class is based on logical operators, with the help of which it builds a query.

Let's analyze the simplest example of how a query is built using Q:

```python
from models_manager import Q

Q(id__in=(1, 2, 3))
'"{model}"."id" IN (1, 2, 3)'
```

From the example above, we can see that our python code has turned into SQL code, thanks to the `Q` class.

- id converted to `"{model}"."id"`
- __in converted to SQL `IN`
- `(1, 2, 3)` converted to SQL `(1, 2, 3)`

---

Now let's complicate the example and add a few more arguments to our `Q`

```python
from models_manager import Q

Q(id__in=(1, 2, 3), id__lt=5)
'"{model}"."id" IN (1, 2, 3) AND "{model}"."id" < 5'
```

- id converted to `"{model}"."id"`
- __lt converted to SQL `<`
- 5 converted to 5

!!! note

    Note that our expressions are now connected with the `AND` operator, 
    which is the default for such expressions. 
    But it can be changed by passing the `default` argument inside our `Q`

```python
from models_manager import Q

Q(id__in=(1, 2, 3), id__lt=5, default=Q.OR)
'"{model}"."id" IN (1, 2, 3) OR "{model}"."id" < 5'
```

Now we see that the expressions are connected via the `OR` operator.

---


Let's now connect the two examples above. To be shared by the `AND` operator

```python
from models_manager import Q

Q(id__in=(1, 2, 3), id__lt=5) | Q(id__in=(1, 2, 3), id__lt=5, default=Q.OR)
"""
("{model}"."id" IN (1, 2, 3) AND "{model}"."id" < 5) 
OR 
("{model}"."id" IN (1, 2, 3) OR "{model}"."id" < 5)
"""
```

We got an example, which is connected, through the `OR` operator

---

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
