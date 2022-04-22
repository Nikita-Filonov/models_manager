class SchemaContext:
    TYPE = 'type'
    ANY_OF = 'anyOf'
    ITEMS = 'items'
    ADDITIONAL_PROPERTIES = 'additionalProperties'
    MIN_ITEMS = 'minItems'
    MAX_ITEMS = 'maxItems'
    CHOICES = 'enum'
    MAX_LENGTH = 'maxLength'
    MIN_LENGTH = 'minLength'
    GT = 'exclusiveMinimum'
    GE = 'minimum'
    LT = 'exclusiveMaximum'
    LE = 'maximum'
    NULL = 'null'

    __slots__ = (
        'choices',
        'max_length',
        'min_length',
        'max_items',
        'min_items',
        'gt',
        'ge',
        'lt',
        'le',
        'title',
        'description',
        '_template',
        'additional_properties',
        'items',
        'any_of',
        'type'
    )

    def __init__(self, **kwargs):
        self._template = {}

        self._apply_kwargs(**kwargs)

    def _apply_kwargs(self, **kwargs):
        for attribute in self.__slots__:
            value = kwargs.get(attribute)

            if value is None:
                continue

            setattr(self, attribute, value)

    @property
    def template(self):
        for attribute in self.__slots__:
            template_key, template_value = getattr(self, attribute.upper(), None), getattr(self, attribute, None)

            if (template_key is None) or (template_value is None):
                continue

            self._template[template_key] = template_value

        return self._template

    @template.setter
    def template(self, value):
        self._template = value
