from pydantic import BaseModel


class ProviderContext(BaseModel):
    """
    Common context which should be passed to provider
    """

    null: bool = False
    max_length: int = None
