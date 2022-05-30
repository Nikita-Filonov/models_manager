import json as json_lib
from functools import lru_cache
from itertools import zip_longest
from typing import Union, List, Tuple, Iterator, Optional

from models_manager import Field
from models_manager.manager.managers.base import BaseManager
from models_manager.utils import deprecated, get_json_from_fields, deep_get

GenericExcludeFields = Optional[List[Union[str, Field]]]


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

    def _field_without_empty_json(self, exclude: GenericExcludeFields = None) -> Iterator:
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

    def to_dict(self, json_key: bool = True, exclude: GenericExcludeFields = None) -> dict:
        safe_exclude = get_json_from_fields(exclude) or self.exclude_dict
        without_empty_json = self._field_without_empty_json(safe_exclude)

        return {
            (field.json if json_key else name): field.dict(json_key, self.ignore_validation)
            for name, field in without_empty_json
        }

    @lru_cache(maxsize=None, typed=True)
    def to_lazy_dict(self, json_key: bool = True, exclude: GenericExcludeFields = None) -> dict:
        return self.to_dict(json_key=json_key, exclude=exclude)

    def to_dump(self, json_key: bool = True, exclude: GenericExcludeFields = None) -> str:
        return json_lib.dumps(self.to_dict(json_key=json_key, exclude=exclude))

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

    def __to_dict_with_negative(self, method: str, fields: GenericExcludeFields = None):
        without_empty_json = self._field_without_empty_json()
        safe_fields = get_json_from_fields(fields)

        return {
            field.json: (
                getattr(field.negative, method)()
                if (field.json in safe_fields)
                else field.dict()
            )
            for _, field in without_empty_json
        }

    def to_dict_with_negative_max_length(self, fields: GenericExcludeFields = None):
        """
        :param fields: List of ``Field`` objects or list of field names in json as strings
        :return: Will return dictionary with fields converted to json,
        where values will negative string more that possible field max length
        """
        return self.__to_dict_with_negative(method='max_length', fields=fields)

    def to_dict_with_negative_min_length(self, fields: GenericExcludeFields = None):
        return self.__to_dict_with_negative(method='min_length', fields=fields)

    def to_dict_with_null_fields(self, fields: GenericExcludeFields = None):
        return self.__to_dict_with_negative(method='null', fields=fields)

    def to_dict_with_empty_string_fields(self, fields: GenericExcludeFields = None):
        return self.__to_dict_with_negative(method='empty_string', fields=fields)

    def to_dict_with_non_unique_fields(
            self,
            payload: dict,
            fields: GenericExcludeFields = None,
            keys: List[List[str]] = None
    ):
        """Used to apply only some values from ``payload`` to given ``fields``."""
        non_unique_fields = {
            field.json: deep_get(payload, *list_of_keys) if list_of_keys else payload[field.json]
            for field, list_of_keys in zip_longest(fields, keys or [])
        }
        return {**self.to_dict(exclude=fields), **non_unique_fields}
