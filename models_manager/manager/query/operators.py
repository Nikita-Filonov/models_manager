from enum import Enum


class SupportedOperators(Enum):
    """
    Query templates, which can be used to constructor model query

    (query template, SQL operator)

    Example:
        MyModel.manager.filter(name__in=('some', 'other'))

        Also can be used inside Q chain
        MyModel.manager.filter(Q(name__in=('some', 'other')) | Q(name='some'))
    """
    IN = '__in', 'IN'
    NOT_IN = '__not_in', 'NOT IN'
    NOT_EQUAL = '__not_equal', '!='
    LT = '__lt', '<'
    LE = '__le', '<='
    GT = '__gt', '>'
    GE = '__ge', '>='
    LIKE = '__like', 'LIKE'

    @classmethod
    def to_list(cls):
        return [template.value for template in cls]
