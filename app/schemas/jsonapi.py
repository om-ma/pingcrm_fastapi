from typing import Any, Dict, Generic, List, Optional, TypeVar, Union
from pydantic import BaseModel, ConfigDict, Field

DataT = TypeVar('DataT')

class JsonApiRelationship(BaseModel):
    data: Optional[Dict[str, Any]] = None
    links: Optional[Dict[str, str]] = None

class JsonApiResource(BaseModel):
    id: str
    type: str
    attributes: Dict[str, Any]
    relationships: Optional[Dict[str, JsonApiRelationship]] = None
    links: Optional[Dict[str, str]] = None

class JsonApiResponse(BaseModel, Generic[DataT]):
    data: Union[DataT, List[DataT]]
    included: Optional[List[JsonApiResource]] = None
    links: Optional[Dict[str, str]] = None
    meta: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "data": {
                    "type": "users",
                    "id": "1",
                    "attributes": {
                        "first_name": "John",
                        "last_name": "Doe",
                        "email": "john@example.com"
                    },
                    "relationships": {
                        "account": {
                            "data": {"type": "accounts", "id": "1"}
                        }
                    }
                }
            }
        }
    )

def create_resource(
    type_name: str,
    id: Union[int, str],
    attributes: Dict[str, Any],
    relationships: Optional[Dict[str, Dict[str, Any]]] = None,
    links: Optional[Dict[str, str]] = None
) -> JsonApiResource:
    """Helper function to create a JSON:API resource object"""
    resource_relationships = {}
    
    if relationships:
        for rel_name, rel_data in relationships.items():
            resource_relationships[rel_name] = JsonApiRelationship(data=rel_data)
    
    return JsonApiResource(
        type=type_name,
        id=str(id),
        attributes=attributes,
        relationships=resource_relationships if resource_relationships else None,
        links=links
    )

def create_response(
    data: Union[JsonApiResource, List[JsonApiResource]],
    included: Optional[List[JsonApiResource]] = None,
    links: Optional[Dict[str, str]] = None,
    meta: Optional[Dict[str, Any]] = None
) -> JsonApiResponse:
    """Helper function to create a JSON:API response"""
    return JsonApiResponse(
        data=data,
        included=included,
        links=links,
        meta=meta
    )
