from enum import Enum


class SupportedOperators(Enum):
    IN = '__in', 'IN'
    NOT_IN = '__not_in', 'NOT IN'
    LT = '__lt', '<'
    LE = '__le', '<='
    GT = '__gt', '>'
    GE = '__ge', '>='
    LIKE = '__like', 'LIKE'

    @classmethod
    def to_list(cls):
        return [template.value for template in cls]
