from typing import Dict, List, Union

import pytest

from models_manager.schema.schema_typing import resolve_typing


@pytest.mark.schema_typing
class TestSchemaTyping:
    @pytest.mark.parametrize('annotation, template', [
        (dict, {'origin': dict, 'args': []}),
        (Dict[str, int], {'origin': dict, 'args': [str, int]}),
        (List[Dict[str, int]], {'origin': list, 'args': [], 'inner': {'origin': dict, 'args': [str, int]}}),
        (List[Dict[str, Union[int, str]]], {
            'origin': list,
            'args': [],
            'inner': {'origin': dict, 'args': [str], 'inner': {'origin': 'union', 'args': [int, str]}}
        })
    ])
    def test_resolve_typing(self, annotation, template):
        assert resolve_typing(annotation) == template
