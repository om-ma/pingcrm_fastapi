from typing import Any, Dict, List, Optional, Type, Union
from sqlalchemy.orm import Session
from app.schemas.jsonapi import JsonApiResource, create_resource

class ModelSerializer:
    """Base serializer class for converting SQLAlchemy models to JSON:API format"""
    
    def __init__(self, type_name: str, attributes: List[str], relationships: Optional[Dict[str, str]] = None):
        self.type_name = type_name
        self.attributes = attributes
        self.relationships = relationships or {}

    def get_attributes(self, obj: Any) -> Dict[str, Any]:
        """Extract attributes from model instance"""
        return {
            attr: getattr(obj, attr)
            for attr in self.attributes
            if hasattr(obj, attr)
        }

    def get_relationships(self, obj: Any, db: Session) -> Dict[str, Dict[str, Any]]:
        """Extract relationships from model instance"""
        relationships = {}
        for rel_name, rel_type in self.relationships.items():
            if hasattr(obj, rel_name):
                related_obj = getattr(obj, rel_name)
                if related_obj:
                    relationships[rel_name] = {
                        "data": {
                            "type": rel_type,
                            "id": str(getattr(related_obj, "id"))
                        }
                    }
        return relationships

    def serialize(self, obj: Any, db: Session) -> JsonApiResource:
        """Convert a single model instance to JSON:API format"""
        return create_resource(
            type_name=self.type_name,
            id=obj.id,
            attributes=self.get_attributes(obj),
            relationships=self.get_relationships(obj, db)
        )

    def serialize_many(self, objects: List[Any], db: Session) -> List[JsonApiResource]:
        """Convert multiple model instances to JSON:API format"""
        return [self.serialize(obj, db) for obj in objects]
