import pytest

from models_manager.utils import random_number, random_string
from tests.model import DefaultModel, DefaultModelAttributes


@pytest.mark.model_object
class TestModelObject:
    @pytest.mark.parametrize('json', [
        DefaultModel.manager.to_json,
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
