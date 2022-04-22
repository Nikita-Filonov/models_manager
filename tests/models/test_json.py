import pytest

from models_manager import Field
from models_manager.utils import random_string
from tests.model import DefaultModel, RandomModal


@pytest.mark.model_json
class TestJSON:
    model = DefaultModel.manager
    random_model = RandomModal.manager

    def test_json_generation(self):
        json = self.model.to_json

        assert json[DefaultModel.id.json] == DefaultModel.id.default
        assert json[DefaultModel.first_name.json] == DefaultModel.first_name.default
        assert json[DefaultModel.email.json] == DefaultModel.email.default

    def test_json_attribute(self):
        json_name = random_string()
        field = Field(json=json_name)

        assert field.json == json_name

    @pytest.mark.parametrize('payload', [model.to_json, {}])
    def test_json_object_generation(self, payload):
        json = DefaultModel(**payload).manager.to_json

        assert json[DefaultModel.id.json] == DefaultModel.id.default
        assert json[DefaultModel.first_name.json] == DefaultModel.first_name.default
        assert json[DefaultModel.email.json] == DefaultModel.email.default

    def test_ability_to_generate_random_json_multiple_times(self):
        json, next_json = self.random_model.to_json, self.random_model.to_json

        assert json != next_json
