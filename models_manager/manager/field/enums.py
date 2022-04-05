from enum import Enum
from typing import List, Any


class FiledGenericEnum(Enum):

    @classmethod
    def to_list(cls) -> List[Any]:
        return [lti.value for lti in cls]
