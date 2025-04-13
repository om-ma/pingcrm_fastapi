from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas.schemas import ContactCreate
from app.schemas.jsonapi import JsonApiResponse, JsonApiResource
from app.serializers.contact import contact_serializer

router = APIRouter()

@router.get("/", response_model=JsonApiResponse[JsonApiResource])
def read_contacts(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve contacts.
    """
    contacts = crud.contact.get_multi(db, skip=skip, limit=limit)
    resources = contact_serializer.serialize_many(contacts, db)
    
    return JsonApiResponse(
        data=resources,
        meta={"total": len(contacts)},
        links={
            "self": f"/api/v1/contacts?skip={skip}&limit={limit}",
            "first": "/api/v1/contacts?skip=0&limit={limit}",
        }
    )

@router.post("/", response_model=JsonApiResponse[JsonApiResource])
def create_contact(
    *,
    db: Session = Depends(deps.get_db),
    contact_in: ContactCreate,
) -> Any:
    """
    Create new contact.
    """
    contact = crud.contact.create(db=db, obj_in=contact_in)
    resource = contact_serializer.serialize(contact, db)
    
    return JsonApiResponse(
        data=resource,
        links={"self": f"/api/v1/contacts/{contact.id}"}
    )

@router.get("/{contact_id}", response_model=JsonApiResponse[JsonApiResource])
def read_contact(
    *,
    db: Session = Depends(deps.get_db),
    contact_id: int,
) -> Any:
    """
    Get contact by ID.
    """
    contact = crud.contact.get(db=db, id=contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    resource = contact_serializer.serialize(contact, db)
    
    return JsonApiResponse(
        data=resource,
        links={"self": f"/api/v1/contacts/{contact_id}"}
    )

@router.put("/{contact_id}", response_model=JsonApiResponse[JsonApiResource])
def update_contact(
    *,
    db: Session = Depends(deps.get_db),
    contact_id: int,
    contact_in: ContactCreate,
) -> Any:
    """
    Update a contact.
    """
    contact = crud.contact.get(db=db, id=contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    contact = crud.contact.update(db=db, db_obj=contact, obj_in=contact_in)
    resource = contact_serializer.serialize(contact, db)
    
    return JsonApiResponse(
        data=resource,
        links={"self": f"/api/v1/contacts/{contact_id}"}
    )

@router.delete("/{contact_id}", response_model=JsonApiResponse[JsonApiResource])
def delete_contact(
    *,
    db: Session = Depends(deps.get_db),
    contact_id: int,
) -> Any:
    """
    Delete a contact.
    """
    contact = crud.contact.get(db=db, id=contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    contact = crud.contact.remove(db=db, id=contact_id)
    resource = contact_serializer.serialize(contact, db)
    
    return JsonApiResponse(
        data=resource,
        links={"self": f"/api/v1/contacts/{contact_id}"}
    )
