from typing import Union, List, Tuple, Iterator

from models_manager import Field
from models_manager.manager.managers.base import BaseManager
from models_manager.utils import deprecated, get_json_from_fields


class JsonManager(BaseManager):

    def __init__(self, model, mro, **kwargs):
        super().__init__(model, mro, **kwargs)

        self._exclude_dict = None
        self._ignore_validation = False

    @property
    def exclude_dict(self):
        return get_json_from_fields(self._exclude_dict)

    @exclude_dict.setter
    def exclude_dict(self, value):
        self._exclude_dict = value

    @property
    def ignore_validation(self):
        return self._ignore_validation

    @ignore_validation.setter
    def ignore_validation(self, value):
        self._ignore_validation = value

    def _field_without_empty_json(self, exclude=None) -> Iterator:
        safe_exclude = exclude or []
        fields = self._fields_as_original()
        return filter(
            lambda args: (args[1].json is not None) and (args[1].json not in safe_exclude),
            fields.items()
        )

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

    def to_dict(self, json_key=True, exclude=None) -> dict:
        safe_exclude = get_json_from_fields(exclude) or self.exclude_dict
        without_empty_json = self._field_without_empty_json(safe_exclude)

        return {
            (field.json if json_key else name): field.dict(json_key, self.ignore_validation)
            for name, field in without_empty_json
        }

    @deprecated('Use "to_dict_with_negative_max_length", "to_dict_with_negative_min_length" instead')
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

    def __to_dict_with_negative(self, method, fields=None):
        without_empty_json = self._field_without_empty_json()
        safe_fields = get_json_from_fields(fields)

        return {
            field.json: (
                getattr(field.negative, method)()
                if (field.json in safe_fields)
                else field.dict(ignore_validation=True)
            )
            for name, field in without_empty_json
        }

    def to_dict_with_negative_max_length(self, fields=None):
        return self.__to_dict_with_negative(method='max_length', fields=fields)

    def to_dict_with_negative_min_length(self, fields=None):
        return self.__to_dict_with_negative(method='min_length', fields=fields)
