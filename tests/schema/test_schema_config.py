import pytest
from tests.model import DefaultModel, ModelWithConfig


@pytest.mark.schema_config
class TestSchemaConfig:
    default_model = DefaultModel.manager
    model_with_config = ModelWithConfig.manager

    def test_schema_do_not_allow_additional_properties(self):
        schema = self.model_with_config.to_schema

        assert not schema.get("additionalProperties")

    def test_schema_allow_additional_properties(self):
        schema = self.default_model.to_schema

        assert schema.get("additionalProperties") is None
