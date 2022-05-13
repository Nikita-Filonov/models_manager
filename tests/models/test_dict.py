import json

import pytest

from models_manager import Field
from models_manager.utils import random_string, random_number
from tests.model import DefaultModel, RandomModal, OuterModel, InnerModel, ListOuterModel, NestedOuterModel, \
    OptionalOuterModel


@pytest.mark.model_dict
class TestDict:
    model = DefaultModel.manager
    random_model = RandomModal.manager

    def test_dict_generation(self):
        json = self.model.to_dict()

        assert json[DefaultModel.id.json] == DefaultModel.id.default
        assert json[DefaultModel.first_name.json] == DefaultModel.first_name.default
        assert json[DefaultModel.email.json] == DefaultModel.email.default

    def test_dict_generation_for_nested_model(self):
        inner = InnerModel(id=random_number())
        outer = OuterModel(inner=inner)

        assert outer.manager.to_dict() == {
            OuterModel.id.json: outer.id.value,
            OuterModel.inner.json: inner.manager.to_dict()
        }

    def test_dict_generation_for_list_nested_model(self):
        inners = [InnerModel(id=random_number()) for _ in range(5)]
        list_outer = ListOuterModel(inners=inners)

        assert list_outer.inners.value == inners
        assert list_outer.manager.to_dict() == {
            ListOuterModel.id.json: list_outer.id.value,
            ListOuterModel.inners.json: [inner.manager.to_dict() for inner in inners]
        }

    def test_dict_generation_for_dict_nested_model(self):
        inner = {'str': InnerModel(id=random_number())}
        dict_outer = NestedOuterModel(inner=inner)

        assert dict_outer.inner.value == inner
        assert dict_outer.manager.to_dict() == {
            NestedOuterModel.id.json: dict_outer.id.value,
            NestedOuterModel.inner.json: {'str': inner['str'].manager.to_dict()}
        }

    def test_dict_generation_for_optional_model(self):
        optional_outer = OptionalOuterModel(inner_or_null=None)

        assert optional_outer.inner_or_null.value is None
        assert optional_outer.manager.to_dict() == {
            OptionalOuterModel.id.json: optional_outer.id.value,
            OptionalOuterModel.inner_or_null.json: None
        }

    def test_json_attribute(self):
        json_name = random_string()
        field = Field(json=json_name)

        assert field.json == json_name

    @pytest.mark.parametrize('payload', [model.to_dict(), {}])
    def test_dict_object_generation(self, payload):
        json = DefaultModel(**payload).manager.to_dict()

        assert json[DefaultModel.id.json] == DefaultModel.id.default
        assert json[DefaultModel.first_name.json] == DefaultModel.first_name.default
        assert json[DefaultModel.email.json] == DefaultModel.email.default

    def test_ability_to_generate_random_json_multiple_times(self):
        json, next_json = self.random_model.to_dict(), self.random_model.to_dict()

        assert json != next_json

    @pytest.mark.parametrize('json_key, expected', [
        (True, {
            DefaultModel.id.json: DefaultModel.id.default,
            DefaultModel.first_name.json: DefaultModel.first_name.default,
            DefaultModel.email.json: DefaultModel.email.default
        }),
        (False, {
            DefaultModel.id.json: DefaultModel.id.default,
            'first_name': DefaultModel.first_name.default,
            DefaultModel.email.json: DefaultModel.email.default
        })
    ])
    def test_field_get_dict_with_json_key(self, json_key, expected):
        assert self.model.to_dict(json_key=json_key) == expected

    @pytest.mark.parametrize('field', [RandomModal.email, RandomModal.first_name])
    def test_get_dict_with_negative_max_length(self, field):
        negative_payload = self.random_model.to_dict_with_negative_max_length(fields=[field])

        assert len(negative_payload[field.json]) > field.max_length

    @pytest.mark.parametrize('field', [RandomModal.email, RandomModal.first_name])
    def test_get_dict_with_negative_min_length(self, field):
        negative_payload = self.random_model.to_dict_with_negative_min_length(fields=[field])

        assert len(negative_payload[field.json]) < field.max_length

    @pytest.mark.parametrize('field', [RandomModal.email, RandomModal.id])
    def test_get_dict_with_null_fields(self, field):
        negative_payload = self.random_model.to_dict_with_null_fields(fields=[field])

        assert negative_payload[field.json] is None

    @pytest.mark.parametrize('field', [RandomModal.email, RandomModal.id])
    def test_get_dict_with_empty_string_fields(self, field):
        negative_payload = self.random_model.to_dict_with_empty_string_fields(fields=[field])

        assert negative_payload[field.json] == ''

    def test_to_lazy_dict(self):
        assert self.random_model.to_lazy_dict() == self.random_model.to_lazy_dict()

    def test_to_dump(self):
        payload_dict = self.model.to_dict()
        payload_dump = self.model.to_dump()

        assert json.dumps(payload_dict) == payload_dump

    @pytest.mark.parametrize('payload, fields', [
        (random_model.to_dict(), [DefaultModel.email]),
        (random_model.to_dict(), [DefaultModel.email, DefaultModel.id]),
        (random_model.to_dict(), [DefaultModel.email, DefaultModel.id, DefaultModel.first_name]),
    ])
    def test_to_dict_with_non_unique_fields(self, payload, fields):
        non_unique_payload = self.model.to_dict_with_non_unique_fields(payload=payload, fields=fields)

        assert all(non_unique_payload[field.json] == payload[field.json] for field in fields)
