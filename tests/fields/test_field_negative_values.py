from typing import Optional

import pytest

from models_manager import Field
from models_manager.manager.exceptions import NegativeValuesException


@pytest.mark.field_negative_values
class TestFieldNegativeValues:
    @pytest.mark.parametrize('attributes', [
        {'category': int, 'max_length': 100},
        {'category': str},
        {'category': Optional[str]},
        {'category': Optional[int]}
    ])
    def test_field_negative_max_length_with_wrong_category(self, attributes):
        field = Field(**attributes)
        with pytest.raises(NegativeValuesException):
            field.negative.max_length()

    @pytest.mark.parametrize('attributes', [
        {'category': int, 'min_length': 100},
        {'category': str},
        {'category': Optional[str]},
        {'category': Optional[int]}
    ])
    def test_field_negative_min_length_with_wrong_category(self, attributes):
        field = Field(**attributes)
        with pytest.raises(NegativeValuesException):
            field.negative.min_length()

    def test_field_negative_max_length(self):
        field = Field(category=str, max_length=100)
        assert len(field.negative.max_length()) > 100

    def test_field_negative_min_length(self):
        field = Field(category=str, min_length=100)
        assert len(field.negative.min_length()) < 100

    @pytest.mark.parametrize('gt', [100, 10, 50])
    def test_field_negative_gt(self, gt):
        field = Field(category=int, gt=gt)

        assert isinstance(field.negative.gt(), float)
        assert field.negative.gt() < gt

    @pytest.mark.parametrize('lt', [100, 10, 50])
    def test_field_negative_lt(self, lt):
        field = Field(category=int, lt=lt)

        assert isinstance(field.negative.lt(), float)
        assert field.negative.lt() > lt

    @pytest.mark.parametrize('ge', [100, 10, 50])
    def test_field_negative_ge(self, ge):
        field = Field(category=int, ge=ge)

        assert isinstance(field.negative.ge(), float)
        assert field.negative.ge() <= ge

    @pytest.mark.parametrize('le', [100, 10, 50])
    def test_field_negative_le(self, le):
        field = Field(category=int, le=le)

        assert isinstance(field.negative.le(), float)
        assert field.negative.le() >= le

    @pytest.mark.parametrize('attributes', [
        {'category': str, 'lt': 100},
        {'category': int},
        {'category': Optional[str]},
        {'category': Optional[int]}
    ])
    def test_field_negative_lt_with_wrong_category(self, attributes):
        field = Field(**attributes)
        with pytest.raises(NegativeValuesException):
            field.negative.lt()

    @pytest.mark.parametrize('attributes', [
        {'category': str, 'gt': 100},
        {'category': int},
        {'category': Optional[str]},
        {'category': Optional[int]}
    ])
    def test_field_negative_gt_with_wrong_category(self, attributes):
        field = Field(**attributes)
        with pytest.raises(NegativeValuesException):
            field.negative.gt()

    @pytest.mark.parametrize('attributes', [
        {'category': str, 'le': 100},
        {'category': int},
        {'category': Optional[str]},
        {'category': Optional[int]}
    ])
    def test_field_negative_le_with_wrong_category(self, attributes):
        field = Field(**attributes)
        with pytest.raises(NegativeValuesException):
            field.negative.le()

    @pytest.mark.parametrize('attributes', [
        {'category': str, 'ge': 100},
        {'category': int},
        {'category': Optional[str]},
        {'category': Optional[int]}
    ])
    def test_field_negative_ge_with_wrong_category(self, attributes):
        field = Field(**attributes)
        with pytest.raises(NegativeValuesException):
            field.negative.ge()

    def test_field_negative_null_value(self):
        field = Field()
        assert field.negative.null() is None

    @pytest.mark.parametrize('choices, category', [
        ([1, 2, 3, 4, 5], int),
        (['1', '2', '3', '4', '5'], str),
        ([1.5, 2.5, 3.5, 4.5, 5.5], float),
    ])
    def test_field_negative_choices_values(self, choices, category):
        field = Field(choices=choices, category=category)

        assert field.negative.choices() not in choices

    def test_field_negative_choices_without_choices_attribute(self):
        field = Field(category=int)
        with pytest.raises(NegativeValuesException):
            field.negative.choices()
