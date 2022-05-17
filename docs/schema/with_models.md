List of object
---

```python
from typing import List

from models_manager import Model, Field


class Task(Model):
    id = Field(json='id', category=int)
    title = Field(json='title', category=str)


class Course(Model):
    id = Field(json='id', category=int)
    title = Field(json='title', category=str)
    tasks = Field(json='tasks', category=List[Task])


Course.manager.to_schema
{
    'title': 'Course',
    'type': 'object',
    'properties': {
        'id': {'type': 'number'},
        'title': {'type': 'string'},
        'tasks': {
            'items': {
                'title': 'Task',
                'type': 'object',
                'properties': {
                    'id': {'type': 'number'},
                    'title': {'type': 'string'}
                },
                'required': ['id', 'title']
            },
            'type': 'array'
        }
    },
    'required': ['id', 'title', 'tasks']
}
```

Here we see `List[Task]`, this type describes a list with Task objects

Let's take a closer look at the json schema

This schema describes the external `Course` object.

```python
{
    'title': 'Course',
    'type': 'object',
    'properties': {
        'id': {'type': 'number'},
        'title': {'type': 'string'},
        'tasks': {
            ...
        }
    },
    'required': ['id', 'title', 'tasks']
}
```

Inside the `Course` object, there is a nested list of Tasks objects. Below we see a schema nested schema of a list of
`Tasks` objects

```python
...
'tasks': {
    'items': {
        'title': 'Task',
        'type': 'object',
        'properties': {
            'id': {'type': 'number'},
            'title': {'type': 'string'}
        },
        'required': ['id', 'title']
    },
    'type': 'array'
}
...
```

Single object
---

```python
from models_manager import Model, Field


class Task(Model):
    id = Field(json='id', category=int)
    title = Field(json='title', category=str)


class Course(Model):
    id = Field(json='id', category=int)
    title = Field(json='title', category=str)
    task = Field(json='task', category=Task)


Course.manager.to_schema
{
    'title': 'Course',
    'type': 'object',
    'properties': {
        'id': {'type': 'number'},
        'title': {'type': 'string'},
        'task': {
            'title': 'Task',
            'type': 'object',
            'properties': {
                'id': {'type': 'number'},
                'title': {'type': 'string'}
            },
            'required': ['id', 'title']
        }
    },
    'required': ['id', 'title', 'task']
}
```

Nested types with model

```python
from typing import Dict, Optional

from models_manager import Model, Field


class Task(Model):
    id = Field(json='id', category=int)
    title = Field(json='title', category=str)


class Course(Model):
    id = Field(json='id', category=int)
    title = Field(json='title', category=str)
    task = Field(json='task', category=Dict[str, Optional[Task]])


Course.manager.to_schema
{
    'title': 'Course',
    'type': 'object',
    'properties': {
        'id': {'type': 'number'},
        'title': {'type': 'string'},
        'task': {
            'additionalProperties': {
                'anyOf': [
                    {
                        'title': 'Task',
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'number'},
                            'title': {'type': 'string'}
                        },
                        'required': ['id', 'title']
                    },
                    {'type': 'null'}
                ]
            },
            'type': 'object'}
    },
    'required': ['id', 'title', 'task']
}
```
