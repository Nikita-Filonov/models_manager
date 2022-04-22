import uuid

from models_manager import Model, Field, FieldGenericEnum
from models_manager.utils import random_string


class DefaultModelAttributes(FieldGenericEnum):
    MANAGER = 'manager'
    IDENTITY = 'identity'
    DATABASE = 'database'
    EXTENDED_BY = 'extended_by'


class DefaultChoices(FieldGenericEnum):
    JUNIOR = 'junior'
    MIDDLE = 'middle'
    SENIOR = 'senior'
    EXPERT = 'expert'


class DefaultModel(Model):
    id = Field(default=1, json='id', category=int)
    first_name = Field(default='some name', json='firstName', category=str)
    email = Field(default='some@gmail.com', json='email', category=str)


class RandomModal(Model):
    id = Field(default=uuid.uuid4, json='id', category=int)
    first_name = Field(default=random_string, json='firstName', category=str)
    email = Field(default=random_string, json='email', category=str)
