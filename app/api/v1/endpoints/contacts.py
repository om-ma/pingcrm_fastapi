from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models
from app.api import deps
from app.schemas.schemas import ContactCreate, ContactUpdate
from app.schemas.jsonapi import JsonApiResponse, JsonApiResource, JsonApiRequest
from app.serializers.contact import contact_serializer
from app.core.exceptions import NotFoundException, ValidationException

router = APIRouter()

@router.get("/", response_model=JsonApiResponse[List[JsonApiResource]])
def read_contacts(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    contacts = crud.contact.get_multi(db, skip=skip, limit=limit)
    resources = [contact_serializer.serialize(contact, db) for contact in contacts]
    
    return JsonApiResponse(
        data=resources,
        meta={"total": len(contacts)},
        links={
            "self": f"/api/v1/contacts?skip={skip}&limit={limit}",
            "first": f"/api/v1/contacts?skip=0&limit={limit}",
        }
    )

@router.post("/", response_model=JsonApiResponse[JsonApiResource])
def create_contact(
    *,
    db: Session = Depends(deps.get_db),
    request: JsonApiRequest,
) -> Any:
    attrs = request.data.attributes
    contact_in = ContactCreate(
        first_name=attrs.first_name,
        last_name=attrs.last_name,
        organization_id=attrs.organization_id,
        email=attrs.email,
        phone=attrs.phone,
        address=attrs.address,
        city=attrs.city,
        region=attrs.region,
        country=attrs.country,
        postal_code=attrs.postal_code,
    )
    
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
    contact = crud.contact.get_or_404(db=db, id=contact_id)
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
    request: JsonApiRequest,
) -> Any:
    contact = crud.contact.get_or_404(db=db, id=contact_id)

    attrs = request.data.attributes
    contact_in = ContactUpdate(
        first_name=attrs.get("first_name", contact.first_name),
        last_name=attrs.get("last_name", contact.last_name),
        organization_id=attrs.get("organization_id", contact.organization_id),
        email=attrs.get("email", contact.email),
        phone=attrs.get("phone", contact.phone),
        address=attrs.get("address", contact.address),
        city=attrs.get("city", contact.city),
        region=attrs.get("region", contact.region),
        country=attrs.get("country", contact.country),
        postal_code=attrs.get("postal_code", contact.postal_code),
    )
    
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
    contact = crud.contact.get_or_404(db=db, id=contact_id)
    contact = crud.contact.remove(db=db, id=contact_id)
    resource = contact_serializer.serialize(contact, db)
    
    return JsonApiResponse(
        data=resource,
        links={"self": f"/api/v1/contacts/{contact_id}"}
    )
