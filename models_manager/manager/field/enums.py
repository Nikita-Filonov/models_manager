from enum import Enum
from typing import List, Any, Optional


class FieldGenericEnum(Enum):

    @classmethod
    def to_list(cls, exclude: Optional[List['FieldGenericEnum']] = None) -> List[Any]:
        safe_exclude = exclude or []
        return [enum.value for enum in cls if enum not in safe_exclude]
