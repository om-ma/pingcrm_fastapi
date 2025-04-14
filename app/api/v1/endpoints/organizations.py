from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models
from app.api import deps
from app.schemas.schemas import OrganizationCreate
from app.schemas.jsonapi import JsonApiResponse, JsonApiResource, JsonApiRequest
from app.serializers.organization import organization_serializer

router = APIRouter()

@router.get("/", response_model=JsonApiResponse[List[JsonApiResource]])
def read_organizations(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    organizations = crud.organization.get_multi(db, skip=skip, limit=limit)
    resources = [organization_serializer.serialize(org, db) for org in organizations]
    
    return JsonApiResponse(
        data=resources,
        meta={"total": len(organizations)},
        links={
            "self": f"/api/v1/organizations?skip={skip}&limit={limit}",
            "first": f"/api/v1/organizations?skip=0&limit={limit}",
        }
    )

@router.post("/", response_model=JsonApiResponse[JsonApiResource])
def create_organization(
    *,
    db: Session = Depends(deps.get_db),
    request: JsonApiRequest,
) -> Any:
    attrs = request.data.attributes
    org_in = OrganizationCreate(
        name=attrs.name,
        email=attrs.email,
        phone=attrs.phone,
        address=attrs.address,
        city=attrs.city,
        region=attrs.region,
        country=attrs.country,
        postal_code=attrs.postal_code,
    )
    
    organization = crud.organization.create(db=db, obj_in=org_in)
    resource = organization_serializer.serialize(organization, db)
    
    return JsonApiResponse(
        data=resource,
        links={"self": f"/api/v1/organizations/{organization.id}"}
    )

@router.get("/{organization_id}", response_model=JsonApiResponse[JsonApiResource])
def read_organization(
    *,
    db: Session = Depends(deps.get_db),
    organization_id: int,
) -> Any:
    organization = crud.organization.get_or_404(db=db, id=organization_id)
    resource = organization_serializer.serialize(organization, db)
    
    return JsonApiResponse(
        data=resource,
        links={"self": f"/api/v1/organizations/{organization_id}"}
    )

@router.put("/{organization_id}", response_model=JsonApiResponse[JsonApiResource])
def update_organization(
    *,
    db: Session = Depends(deps.get_db),
    organization_id: int,
    request: JsonApiRequest,
) -> Any:
    organization = crud.organization.get_or_404(db=db, id=organization_id)

    attrs = request.data.attributes
    org_in = OrganizationCreate(
        name=attrs.name,
        email=attrs.email,
        phone=attrs.phone,
        address=attrs.address,
        city=attrs.city,
        region=attrs.region,
        country=attrs.country,
        postal_code=attrs.postal_code,
    )
    
    organization = crud.organization.update(db=db, db_obj=organization, obj_in=org_in)
    resource = organization_serializer.serialize(organization, db)
    
    return JsonApiResponse(
        data=resource,
        links={"self": f"/api/v1/organizations/{organization_id}"}
    )

@router.delete("/{organization_id}", response_model=JsonApiResponse[JsonApiResource])
def delete_organization(
    *,
    db: Session = Depends(deps.get_db),
    organization_id: int,
) -> Any:
    organization = crud.organization.remove(db=db, id=organization_id)
    resource = organization_serializer.serialize(organization, db)
    
    return JsonApiResponse(
        data=resource,
        links={"self": f"/api/v1/organizations/{organization_id}"}
    )
