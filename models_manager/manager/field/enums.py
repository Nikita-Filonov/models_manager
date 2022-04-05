from enum import Enum


class FiledGenericEnum(Enum):

    @classmethod
    def choices(cls):
        return [lti.value for lti in cls]
