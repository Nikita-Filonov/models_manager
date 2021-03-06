import uuid
from typing import Dict, List, Optional

from models_manager import Field, FieldGenericEnum, Model
from models_manager.utils import random_string


class DefaultModelAttributes(FieldGenericEnum):
    MANAGER = "manager"
    IDENTITY = "identity"
    DATABASE = "database"
    EXTENDED_BY = "extended_by"


class DefaultChoices(FieldGenericEnum):
    JUNIOR = "junior"
    MIDDLE = "middle"
    SENIOR = "senior"
    EXPERT = "expert"


class DefaultModel(Model):
    id = Field(default=1, json="id", category=int)
    first_name = Field(default="some name", json="firstName", category=str)
    email = Field(default="some@gmail.com", json="email", category=str)


class RandomModal(Model):
    id = Field(default=uuid.uuid4, json="id", category=str)
    first_name = Field(
        default=random_string,
        json="firstName",
        category=str,
        max_length=200,
        min_length=10,
    )
    email = Field(
        default=random_string, json="email", category=str, max_length=100, min_length=10
    )


class InnerModel(Model):
    id = Field(default=1, json="id", category=int)


class OuterModel(Model):
    id = Field(default=1, json="id", category=int)
    inner = Field(json="inner", category=InnerModel, default=InnerModel)


class ListOuterModel(Model):
    id = Field(default=1, json="id", category=int)
    inners = Field(json="inners", category=List[InnerModel], default=InnerModel)


class NestedOuterModel(Model):
    id = Field(default=1, json="id", category=int)
    inner = Field(json="inner", category=Dict[str, InnerModel])


class OptionalOuterModel(Model):
    id = Field(default=1, json="id", category=int)
    inner_or_null = Field(json="inner_or_null", category=Optional[InnerModel])


class OptionalFieldModel(Model):
    email = Field(json="email", category=str)
    username = Field(json="username", optional=True, category=str)


class ModelWithConfig(Model):
    email = Field(json="email", category=str)
    username = Field(json="username", optional=True, category=str)

    class Config:
        additional_properties = False
