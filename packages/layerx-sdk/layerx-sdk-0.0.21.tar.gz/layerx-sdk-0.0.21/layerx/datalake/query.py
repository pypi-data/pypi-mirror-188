import datetime
from typing import TYPE_CHECKING
from .logger import get_debug_logger

if TYPE_CHECKING:
    from . import DatalakeClient

annotation_logger = get_debug_logger('Query')


class Query:
    def __init__(self, client: "DatalakeClient"):
        self._client = client


    def get_selection_id(self, collection_id, query, filter, object_type, object_list):
        if object_list == None:
            object_list = []
        filterData = {
            "contentType": object_type,
            "filterBy": [],
            "date": None
        }
        if("filterBy" in filter):
            filterData["filterBy"] = filter["filterBy"]
            
        if("date" in filter):
            filterData["filterBy"] = filter["date"]
        
        #"metadata.Tags=2.1"
        payload = {
            "isAllSelected": True,
            # "projectType": 3,
            "objectIdList": object_list,
            "filterData": filterData,
            "query": query,
            "collectionId": collection_id
        }
        print(payload)
        response = self._client.datalake_interface.get_selection_id(payload)
        return response