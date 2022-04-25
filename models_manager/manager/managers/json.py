from typing import Union, List, Tuple

from models_manager import Field
from models_manager.manager.managers.base import BaseManager
from models_manager.utils import deprecated


class JsonManager(BaseManager):

    @property
    @deprecated('Use "to_dict" instead')
    def to_json(self) -> dict:
        """
        Returns json payload. To return field in json,
        json property: Field(json='some_value'), should be
        defined.

        Example:
            MyModel.manager.to_json -> {'id': 1, 'username': 'some'}
        """
        return {
            value.json: value.value
            for value in self._fields_as_original().values()
            if value.json is not None
        }

    def to_dict(self, json_key=True) -> dict:
        fields = self._fields_as_original()
        without_empty_json = filter(lambda args: args[1].json is not None, fields.items())
        return {(field.json if json_key else name): field.dict(json_key) for name, field in without_empty_json}

    def to_negative_json(self, fields: Union[List[Field], Tuple[Field]] = None, provider=None) -> dict:
        """
        Same as .to_json, but will return json with negative values

        :param fields: List or tuple of fields that should be returned with negative values.
        By default if fields = None, all fields will be returned with negative values
        :param provider: Provider class that will be applied for all fields
        :return: Dictionary

        Example:
            class MyModel(Model):
                id = Field(default=1, json='id')
                username = Field(json='username', default='some', category=str, null=False)

            MyModel.manager.to_negative_json(fields=[MyModel.username]) -> {'id': '1', 'username': None}
        """
        fields_as_original = self._fields_as_original().values()
        safe_fields = fields or fields_as_original
        return {
            value.json: value.get_negative_values(provider) if value in safe_fields else value.get_default
            for value in fields_as_original
            if value.json is not None
        }
