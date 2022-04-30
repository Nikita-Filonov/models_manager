from datetime import datetime, date, time, timedelta
from typing import Dict, List, Union

import pytest

from models_manager.schema.schema_typing import resolve_typing


@pytest.mark.schema_typing
class TestSchemaTyping:
    @pytest.mark.parametrize('annotation, template', [
        (dict, {'origin': dict, 'args': [], 'inner': None}),
        (Dict[str, int], {'origin': dict, 'args': [str, int], 'inner': None}),
        (List[Dict[str, int]], {
            'origin': list,
            'args': [],
            'inner': {'origin': dict, 'args': [str, int], 'inner': None}
        }),
        (List[Dict[str, Union[int, str]]], {
            'origin': list,
            'args': [],
            'inner': {
                'origin': dict,
                'args': [str],
                'inner': {'origin': 'union', 'args': [str, int], 'inner': None}
            }
        }),
        (None, {'args': [], 'origin': None, 'inner': None}),
        (datetime, {'args': [], 'inner': None, 'origin': datetime}),
        (date, {'args': [], 'inner': None, 'origin': date}),
        (time, {'args': [], 'inner': None, 'origin': time}),
        (timedelta, {'args': [], 'inner': None, 'origin': timedelta})
    ])
    def test_resolve_typing(self, annotation, template):
        assert resolve_typing(annotation).serialize() == template
