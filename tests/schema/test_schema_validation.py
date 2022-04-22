from typing import Union, Optional, Dict, List, Any

import pytest

from models_manager import Field
from models_manager.manager.exeptions import SchemaException


@pytest.mark.schema_validation
class TestSchemaValidation:
    @pytest.mark.parametrize('length', [{'max_length': 10}, {'min_length': 0}, {'min_length': 0, 'max_length': 10}])
    def test_schema_validation_with_min_or_max_length(self, length):
        field = Field(json='some', category=int, **length)
        with pytest.raises(SchemaException):
            field.get_schema

    @pytest.mark.parametrize('items', [{'max_items': 10}, {'min_items': 0}, {'max_items': 0, 'min_items': 10}])
    def test_schema_validation_with_max_or_min_items(self, items):
        field = Field(json='some', category=tuple, **items)
        with pytest.raises(SchemaException):
            field.get_schema

    @pytest.mark.parametrize('items', [
        {'category': str, 'min_items': 10},
        {'category': int, 'min_items': 10},
        {'category': bool, 'min_items': 10},
        {'category': float, 'min_items': 10},
        {'category': None, 'min_items': 10},
        {'category': Union[int, str], 'min_items': 10},
        {'category': Optional[int], 'min_items': 10},
        {'category': Dict[int, str], 'min_items': 10},
        {'category': Dict[int, Union[str, int]], 'min_items': 10},
        {'category': Dict[int, List[str]], 'min_items': 10},
    ])
    def test_schema_validation_with_max_or_min_items_on_non_array_category(self, items):
        field = Field(json='some', **items)
        with pytest.raises(SchemaException):
            field.get_schema

    @pytest.mark.parametrize('gt_or_lt', [
        {'gt': 10},
        {'ge': 0},
        {'lt': 0, 'gt': 10},
        {'lt': 10},
        {'le': 0},
        {'le': 0, 'ge': 10},
        {'le': 0, 'gt': 10}
    ])
    def test_schema_validation_with_gt_ge_lt_le(self, gt_or_lt):
        field = Field(json='some', category=str, **gt_or_lt)
        with pytest.raises(SchemaException):
            field.get_schema

    @pytest.mark.parametrize('gt_or_ge', [{'gt': 0, 'ge': 10}, {'lt': 0, 'le': 10}])
    def test_schema_validation_with_gt_ge_or_lt_le_at_same_time(self, gt_or_ge):
        field = Field(json='some', category=int, **gt_or_ge)
        with pytest.raises(SchemaException):
            field.get_schema

    @pytest.mark.parametrize('choices', [12345, 'some', 123.45, True, {1: 2}])
    def test_schema_validation_with_choices(self, choices: Any):
        field = Field(json='some', category=int, choices=choices)
        with pytest.raises(SchemaException):
            field.get_schema
