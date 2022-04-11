Models can also be used to annotate arguments or return values

```python
import uuid

from requests import post

from models_manager import Model, Field
from models_manager.utils import random_string


class User(Model):
    id = Field(default=1, json='id')
    username = Field(default='some', json='username')
    email = Field(default='email@gmail.com', json='email')


def create_user(user: User) -> User:  # accepting user object
    ...
    user_json = user.manager.to_json  # getting user object as dict
    json_response = post(f'user/{user.id.value}', json=user_json).json()
    return User(**json_response)


new_user = User(**User.manager.to_json)
user = create_user(new_user)  # will return created user object

user.id.value
1
user.username.value
'some'
user.email.value
'email@gmail.com'
```
