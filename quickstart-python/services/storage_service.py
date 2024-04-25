import json
from typing import Any, Dict, List, Union

import monday_code
from monday_code import JsonValue, StorageApi

from models import APITypes
from services import with_monday_api

JSONType = Union[Dict[str, Any], List[Any], str, int, float, bool, None]


class StorageService:
    api_type = APITypes.STORAGE

    def __init__(self, monday_access_token: str):
        self.monday_access_token = monday_access_token

    @with_monday_api(api_type, 'get_by_key_from_storage')
    def get(self, key: str, api_instance: StorageApi = None) -> JSONType:
        api_response = api_instance.get_by_key_from_storage(str(key), self.monday_access_token)
        return json.loads(api_response.value) if api_response else None

    @with_monday_api(api_type, 'upsert_by_key_from_storage')
    def upsert(self, key: str, value: JSONType, version: str, previous_version: str = '',
               shared: bool = False, api_instance: StorageApi = None) -> None:
        json_value = JsonValue(actual_instance=value)
        storage_data_contract = monday_code.StorageDataContract(value=json_value, version=str(version))
        # TODO: Change params order after Shai's PR approval!!
        api_instance.upsert_by_key_from_storage(key=str(key), x_monday_access_token=self.monday_access_token,
                                                shared=shared, previous_version=previous_version,
                                                storage_data_contract=storage_data_contract)

    @with_monday_api(api_type, 'delete_by_key_from_storage')
    def delete(self, key: str, api_instance: StorageApi = None) -> None:
        api_instance.delete_by_key_from_storage(str(key), self.monday_access_token)
