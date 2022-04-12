from models_manager import Model, Field, FieldGenericEnum


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
