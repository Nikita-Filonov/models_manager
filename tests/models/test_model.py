import pytest

from tests.model import DefaultModel, DefaultModelAttributes


@pytest.mark.model
class TestModel:
    @pytest.mark.parametrize('attribute', DefaultModelAttributes.to_list())
    def test_base_model_has_default_attributes(self, attribute):
        assert hasattr(DefaultModel, attribute)
