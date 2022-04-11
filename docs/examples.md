### With object annotation

Let's create an example test that uses models, validation, and json generation.

Imagine that we have several endpoints that allow us to manipulate the user

| Method  | Endpoint         | Body   |
| :------ | :--------------- | :----- |
| GET     | /users           | None |
| POST    | /users           | {'id': 1, 'username': 'some', 'email': 'other'} |
| PUT     | /users/{user_id} | {'id': 1, 'username': 'some', 'email': 'other'} |

This is what the user object looks like

| Field    | Type   | Value        |
| :------- | :----- | :----------- |
| id       | number | Any integer  |
| username | string | Any string   |
| email    | string | Email string |

Let's start by creating a model

`/models/user.py`

```python
from models_manager import Model, Field
from models_manager.utils import random_number, random_string


def get_email() -> str:
    """Generates random email"""
    return random_string() + '@gmail.com'


class User(Model):
    id = Field(default=random_number, json='id', category=int)
    username = Field(default=random_string, json='username', category=str)
    email = Field(default=get_email, json='email', category=str)

```

`/api/users.py`

```python
from models.user import User
from requests import get, post, put, Response


def get_users() -> Response:
    return get('/users')


def create_user(user: User) -> Response:
    json = user.manager.to_json
    return post('/users', json=json)


def update_user(user_id: int, user: User) -> Response:
    json = user.manager.to_json
    return put(f'/users/{user_id}', json=json)
```

`tests/conftest.py`

```python
import pytest
from models.user import User


@pytest.fixture(scope='function')
def user() -> User:
    user_object = User(**User.manager.to_json)

    user_json = create_user(user_object).json()
    return User(**user_json)
```

`tests/test_user.py`

```python
from http import HTTPStatus

import pytest
from api.users import get_users, create_user
from assertions import validate_json
from models.user import User


@pytest.mark.users
class TestUser:
    def test_get_users(self):
        response = get_users()
        json_response = response.json()

        assert response.status_code == HTTPStatus.OK
        validate_json(json_response, User.manager.to_array_schema)

    def test_create_user(self):
        user = User(**User.manager.to_json)

        response = create_user(user)
        json_response = response.json()

        assert response.status_code == HTTPStatus.CREATED
        assert user.id.value == json_response[user.id.json]
        assert user.username.value == json_response[user.username.json]
        assert user.email.value == json_response[user.email.json]
        validate_json(json_response, user.manager.to_schema)

    def test_update_user(self, user: User):  # user object created by fixture
        # creating new user object, with new values, for updating
        update_user = User(**User.manager.to_json)

        # user.id.value - value from fixture
        # updated_user - the user object we use to update
        response = update_user(user.id.value, update_user)
        json_response = response.json()

        assert response.status_code == HTTPStatus.OK
        assert user.id.value == json_response[user.id.json]  # usually we not updating ID
        assert update_user.username.value == json_response[user.username.json]
        assert update_user.email.value == json_response[user.email.json]
        validate_json(json_response, user.manager.to_schema)
```

This example is just a sample of how the models can be used. In fact, the scope is much wider. Some methods in this
example can be overwritten. Let's look at how we can rewrite the user update test

In `update_user` we can use just object to update user

```python hl_lines="1 3"
def update_user(user: User) -> Response:
    json = user.manager.to_json
    return put(f'/users/{user.id.value}', json=json)
```

Then our tests would look like

```python hl_lines="4 6 8 12"

class TestUser:
    ...

    def test_update_user(self, user: User):  # user object created by fixture
        # now we overriding id of update_user object
        update_user = User(**User.manager.to_json, id=user.id.value)

        response = update_user(update_user)
        json_response = response.json()

        assert response.status_code == HTTPStatus.OK
        assert update_user.id.value == json_response[user.id.json]
        assert update_user.username.value == json_response[user.username.json]
        assert update_user.email.value == json_response[user.email.json]
        validate_json(json_response, user.manager.to_schema)
```
