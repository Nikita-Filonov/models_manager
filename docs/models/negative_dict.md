The manager has methods that, based on the model, can generate negative values for fields. Each method accepts a list of
fields and negative values will be generated for fields from the list. The fields in the list can be passed as strings
or `Field` objects

Dict with negative max length
---

Used to generate a negative value that under length will be greater than the maximum length of the field. Applies to
string fields

```python
from models_manager import Model, Field


class User(Model):
    id = Field(json='id', category=int, default=1)
    email = Field(json='email', category=str, max_length=100)
    username = Field(json='username', category=str, max_length=50)


User.manager.to_dict_with_negative_max_length(fields=[User.username, User.email])
{
    'id': 1,
    # len equal to 120
    'email': '0MJJ3emj7oEug3FA66ppFj8uMakPNojwJ8egZqsVwKqAlD9uSPOtgvpSG9UQnL1n5eYHJSSBVC2P00X3TwMzBdYauDYDoSRiPhAMxJE0T7WOJqGhpomTgVRW',
    # len equal to 63
    'username': '04KlqG2SnSsgHfNqTbXckCz2iNA3vwXMAdiPkoLfDAQQZdsN8PKbyMCc0VShFd6'
}
```

Dict with negative min length
---

Used to generate negative values that are less than the minimum field value. Applies to string fields

```python
from models_manager import Model, Field


class User(Model):
    id = Field(json='id', category=int, default=1)
    email = Field(json='email', category=str, min_length=10)
    username = Field(json='username', category=str, min_length=6)


User.manager.to_dict_with_negative_min_length(fields=[User.username, User.email])
{
    'id': 1,
    'email': 'TNiXpglfh',  # len equal to 9
    'username': 'ohOsy'  # len equal to 5
}
```

Dict with null fields
---

Used to generate an object dictionary with negative values equal to `None/null`. Can be applied to any field types

```python
from models_manager import Model, Field


class User(Model):
    id = Field(json='id', category=int, default=1)
    email = Field(json='email', category=str, default='email')
    username = Field(json='username', category=str, default='username')


User.manager.to_dict_with_null_fields(fields=[User.username, User.email])
{
    'id': 1,
    'email': None,
    'username': None
}
```

Dict with empty strings
---

Used to create a dictionary of objects with negative values equal to the empty string `""`. Can be applied to any field
types

```python
from models_manager import Model, Field


class User(Model):
    id = Field(json='id', category=int, default=1)
    email = Field(json='email', category=str, default='email')
    username = Field(json='username', category=str, default='username')


User.manager.to_dict_with_empty_string_fields(fields=[User.username, User.email])
{
    'id': 1,
    'email': '',
    'username': ''
}
```
