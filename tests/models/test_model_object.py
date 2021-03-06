import pytest
from jsonschema.exceptions import ValidationError

from models_manager.utils import random_number, random_string
from tests.model import DefaultModel, DefaultModelAttributes, InnerModel, OuterModel


@pytest.mark.model_object
class TestModelObject:
    EXCLUDE_DICT_PARAMS = [
        (
            [DefaultModel.email],
            {
                DefaultModel.id.json: DefaultModel.id.default,
                DefaultModel.first_name.json: DefaultModel.first_name.default
            }
        ),
        (
            [DefaultModel.first_name, DefaultModel.email],
            {DefaultModel.id.json: DefaultModel.id.default}
        )
    ]

    @pytest.mark.parametrize('json', [
        DefaultModel.manager.to_dict(),
        {
            DefaultModel.id.json: random_number(),
            DefaultModel.email.json: random_string(),
            DefaultModel.first_name.json: random_string()
        }
    ])
    def test_create_model_object_based_on_json(self, json):
        model_object = DefaultModel(**json)

        assert model_object.id.value == json[DefaultModel.id.json]
        assert model_object.email.value == json[DefaultModel.email.json]
        assert model_object.first_name.value == json[DefaultModel.first_name.json]

    def test_create_model_object(self):
        model_object = DefaultModel()

        assert model_object.id.value == DefaultModel.id.default
        assert model_object.email.value == DefaultModel.email.default
        assert model_object.first_name.value == DefaultModel.first_name.default

    @pytest.mark.parametrize('attribute', DefaultModelAttributes.to_list())
    def test_model_object_has_default_attributes(self, attribute):
        model_object = DefaultModel()
        assert hasattr(model_object, attribute)

    @pytest.mark.parametrize('attributes', [
        {DefaultModel.id.json: random_string()},
        {DefaultModel.id.json: True},
        {DefaultModel.id.json: []},
        {DefaultModel.id.json: {}},
        {DefaultModel.id.json: DefaultModel},
    ])
    def test_model_object_value_validation(self, attributes):
        with pytest.raises(ValidationError):
            DefaultModel(**attributes)

    @pytest.mark.parametrize('value', [True, [], {}, DefaultModel, 'some'])
    def test_model_object_field_value_setter_validation(self, value):
        model_object = DefaultModel()

        with pytest.raises(ValidationError):
            model_object.id.value = value

    def test_model_object_for_nested_model(self):
        inner = InnerModel(id=5)
        outer = OuterModel(inner=inner)

        assert outer.inner.value == inner
        assert outer.inner.value.id == inner.id
        assert outer.inner.value.id.value == inner.id.value

    @pytest.mark.parametrize('exclude_dict, expected', EXCLUDE_DICT_PARAMS)
    def test_get_model_object_dict_with_exclude_dict(self, exclude_dict, expected):
        model_object = DefaultModel(exclude_dict=exclude_dict)

        assert model_object.manager.to_dict() == expected

    @pytest.mark.parametrize('exclude_dict, expected', EXCLUDE_DICT_PARAMS)
    def test_get_dict_with_exclude(self, exclude_dict, expected):
        model_object = DefaultModel()

        assert model_object.manager.to_dict(exclude=exclude_dict) == expected

    @pytest.mark.parametrize('exclude_schema, expected', [
        (
                [DefaultModel.email],
                {
                    'properties': {'firstName': {'type': 'string'}, 'id': {'type': 'number'}},
                    'required': ['id', 'firstName'],
                    'title': 'DefaultModel',
                    'type': 'object'
                }
        ),
        (
                [DefaultModel.email, DefaultModel.id],
                {
                    'properties': {'firstName': {'type': 'string'}},
                    'required': ['firstName'],
                    'title': 'DefaultModel',
                    'type': 'object'
                }
        )
    ])
    def test_get_model_object_schema_with_exclude_schema(self, exclude_schema, expected):
        model_object = DefaultModel(exclude_schema=exclude_schema)

        assert model_object.manager.to_schema == expected
