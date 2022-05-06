Using the model, you can describe absolutely any object. The model supports standard python typing. That is, we can use
`List[int]`, `List[str]`, `Union[str, int]` etc.

Currently, most of the python types such as `List`, `Dict`, `Tuple`, `Union`, `Optional` are supported, as well as
models

Any nesting of objects is supported, for example `List[Dict[str, Union[int, bool]]]`

List
---

`List` is used when you can have a list of some objects or just strings or numbers

```python
from typing import List

from models_manager import Model, Field


class User(Model):
    states = Field(json='states', category=List[int])


User.manager.to_schema
{
    'title': 'User',
    'type': 'object',
    'properties': {
        'states': {'items': {'type': 'number'}, 'type': 'array'}
    },
    'required': ['states']
}
```

Dict
---

`Dict` is used when you want to describe some object, the object can contain any fields

```python
from typing import Dict

from models_manager import Model, Field


class User(Model):
    states = Field(json='states', category=Dict[str, int])


User.manager.to_schema
{
    'title': 'User',
    'type': 'object',
    'properties': {
        'states': {
            'additionalProperties': {'type': 'number'},
            'type': 'object'
        }
    },
    'required': ['states']
}
```

Union
---

`Union` is used when you want to describe several types at once. For example, if the field can be a string, a number, a
boolean value, or even an object

```python
from typing import Union

from models_manager import Model, Field


class User(Model):
    states = Field(json='states', category=Union[str, int, bool])


User.manager.to_schema
{
    'title': 'User',
    'type': 'object',
    'properties': {
        'states': {
            'anyOf': [
                {'type': 'string'},
                {'type': 'number'},
                {'type': 'boolean'}
            ]
        }
    },
    'required': ['states']
}
```

Tuple
---

`Tuple` is used when you have a list of a certain length with certain elements

```python
from typing import Tuple

from models_manager import Model, Field


class User(Model):
    states = Field(json='states', category=Tuple[str, int, bool])


User.manager.to_schema
{
    'title': 'User',
    'type': 'object',
    'properties': {
        'states': {
            'maxItems': 3,
            'minItems': 3,
            'items': [
                {'type': 'string'},
                {'type': 'number'},
                {'type': 'boolean'}
            ],
            'type': 'array'
        }
    },
    'required': ['states']
}

```

Optional
---

`Optional` is used when the field can be `null`

```python
from typing import Optional

from models_manager import Model, Field


class User(Model):
    states = Field(json='states', category=Optional[str])


User.manager.to_schema
{
    'title': 'User',
    'type': 'object',
    'properties': {
        'states': {
            'anyOf': [
                {'type': 'string'},
                {'type': 'null'}
            ]
        }
    },
    'required': ['states']
}
```

Nested types
---

Thus, we can describe absolutely any object structure, with any nesting

```python
from typing import List, Dict, Union, Optional

from models_manager import Model, Field


class User(Model):
    states = Field(json='states', category=List[Dict[str, Union[int, str, Optional[bool]]]])


User.manager.to_schema
{
    'title': 'User',
    'type': 'object',
    'properties': {
        'states': {
            'items': {
                'additionalProperties': {
                    'anyOf': [
                        {'type': 'number'},
                        {'type': 'string'},
                        {'type': 'boolean'},
                        {'type': 'null'}
                    ]
                },
                'type': 'object'
            },
            'type': 'array'
        }
    },
    'required': ['states']
}
```
