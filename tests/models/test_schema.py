import pytest

from tests.model import DefaultModel


@pytest.mark.model_object
class TestModelSchema:

    @pytest.mark.parametrize('model, schema', [
        (
                {'model': DefaultModel},
                {
                    'properties': {
                        'email': {'type': 'string'},
                        'firstName': {'type': 'string'},
                        'id': {'type': 'number'}
                    },
                    'required': ['id', 'firstName', 'email'],
                    'title': 'DefaultModel',
                    'type': 'object'
                }
        )
    ])
    def test_model_schema_generation(self, model, schema):
        actual_schema = model['model'].manager.to_schema

        assert actual_schema == schema
