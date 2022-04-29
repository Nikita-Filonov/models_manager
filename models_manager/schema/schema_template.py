class SchemaTemplate:
    __slots__ = ('_origin', '_args', '_inner')

    def __init__(self):
        self._origin = None
        self._args = []
        self._inner = None

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        self._origin = value

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, value):
        self._args = value

    @property
    def inner(self) -> 'SchemaTemplate':
        return self._inner

    @inner.setter
    def inner(self, value):
        self._inner = value

    def __str__(self):
        return f'<{self.__class__.__name__}: {self.origin}>'

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.origin}>'

    def serialize(self):
        result = {}
        for attr in self.__slots__:
            value = getattr(self, attr, None)
            safe_attr = attr.replace('_', '')

            if attr == '_inner' and value is not None:
                result[safe_attr] = value.serialize()
                continue

            result[safe_attr] = value

        return result
