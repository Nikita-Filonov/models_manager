from typing import Optional

from models_manager.manager.query.builder import template_to_query


class Q:
    AND = 'AND'
    OR = 'OR'
    default = AND

    def __init__(self, defined_query: Optional[str] = None, default=AND, **kwargs):
        self._query = kwargs
        self._defined_query = defined_query
        self.default = default

    @property
    def defined_query(self):
        return self._defined_query

    def to_query(self):
        return f' {self.default} '.join([template_to_query(key, value) for key, value in self._query.items()])

    def resolve_query(self, node: Optional['Q'], operator: str):
        if self._defined_query is None:
            self_query, other_query = self.to_query(), node.to_query()
            self._defined_query = f'{self_query} {operator} {other_query}'
            return Q(defined_query=self._defined_query)
        else:
            return Q(defined_query=f'{self._defined_query} {operator} {node.to_query()}')

    def __and__(self, other: 'Q'):
        return self.resolve_query(other, self.AND)

    def __or__(self, other: 'Q'):
        return self.resolve_query(other, self.OR)

    def __str__(self):
        return self._defined_query
