from pydantic import BaseModel

from models_manager.manager.field.typing import GenericCategories


class ProviderContext(BaseModel):
    """
    Common context which should be passed to provider
    """

    null: bool = False
    max_length: int = None


class SchemaProviderContext(BaseModel):
    null: bool = False
    max_length: int = None
    category: GenericCategories = str
    is_nullable: bool = False
    is_related: bool = False
