from typing import Optional, List, Dict, Union, Tuple

import pytest

from models_manager import Field
from models_manager.manager.exeptions import FieldException
from models_manager.manager.field.typing import SUPPORTED_TYPES
from models_manager.utils import random_string
from tests.model import DefaultChoices


@pytest.mark.field
class TestField:

    @pytest.mark.parametrize('type_name, default', [
        (category, {} if issubclass(category, dict) else '100')
        for category in SUPPORTED_TYPES
    ])
    def test_field_category(self, type_name, default):
        field = Field(default=default, category=type_name)

        assert field.category == type_name
        assert field.value == type_name(field.default)

    def test_field_with_not_supported_category(self):
        field = Field(default=random_string(), category=Field)
        with pytest.raises(FieldException):
            field.value

    def test_field_value_getter(self):
        default = random_string()
        field = Field(default=default, category=str)

        assert field.value == default

    def test_field_value_setter(self):
        value = random_string()
        field = Field(category=str)
        field.value = value

        assert field.value == value

    def test_field_choices(self):
        field = Field(default=DefaultChoices.EXPERT.value, choices=DefaultChoices.to_list())
        field.value = DefaultChoices.JUNIOR.value

        assert field.value == DefaultChoices.JUNIOR.value
        assert field.choices == DefaultChoices.to_list()

    def test_field_choice_with_not_supported_choice(self):
        field = Field(json='some', default=DefaultChoices.EXPERT.value, choices=DefaultChoices.to_list())

        with pytest.raises(FieldException):
            field.value = random_string()

    def test_callable_as_default(self):
        field = Field(default=lambda: 'some')

        assert field.value == 'some'
        assert callable(field.default)

    @pytest.mark.parametrize('arguments, schema', [
        (
                {'max_length': 255, 'min_length': 100, 'category': str},
                {'maxLength': 255, 'minLength': 100, 'type': 'string'}
        ),
        ({'category': int, 'le': 0, 'gt': 10}, {'exclusiveMinimum': 10, 'maximum': 0, 'type': 'number'}),
        ({'category': int, 'lt': 0, 'gt': 10}, {'exclusiveMaximum': 0, 'exclusiveMinimum': 10, 'type': 'number'}),
        ({'category': int, 'le': 0, 'ge': 10}, {'maximum': 0, 'minimum': 10, 'type': 'number'}),
        ({'category': int, 'le': 0, 'gt': 10}, {'exclusiveMinimum': 10, 'maximum': 0, 'type': 'number'}),
        ({'category': int}, {'type': 'number'}),
        ({'category': float}, {'type': 'number'}),
        ({'category': list}, {'type': 'array', 'items': {}}),
        ({'category': tuple}, {'type': 'array'}),
        ({'category': dict}, {'type': 'object'}),
        ({'category': bool}, {'type': 'boolean'}),
        ({'category': None}, {'type': 'null'}),
        ({'category': Optional[int]}, {'anyOf': [{'type': 'number'}, 'null']}),
        ({'category': Optional[str]}, {'anyOf': [{'type': 'string'}, 'null']}),
        ({'category': Optional[list]}, {'anyOf': [{'type': 'array'}, 'null']}),
        ({'category': List[str]}, {'type': 'array', 'items': {'type': 'string'}}),
        (
                {'category': Dict[str, Union[int, bool]]},
                {'type': 'object', 'additionalProperties': {'anyOf': [{'type': 'number'}, {'type': 'boolean'}]}}
        ),
        ({'category': Union[str, int, bool]}, {'anyOf': [{'type': 'string'}, {'type': 'number'}, {'type': 'boolean'}]}),
        (
                {'category': Tuple[int, str, list]},
                {
                    'type': 'array',
                    'minItems': 3,
                    'maxItems': 3,
                    'items': [{'type': 'number'}, {'type': 'string'}, {'type': 'array'}]
                }
        )
    ], ids=lambda param: str(param))
    def test_field_get_schema(self, arguments, schema):
        field = Field(json='some', **arguments)
        assert field.get_schema == schema
