from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas.schemas import OrganizationCreate
from app.schemas.jsonapi import JsonApiResponse, JsonApiResource
from app.serializers.organization import organization_serializer

router = APIRouter()

@router.get("/", response_model=JsonApiResponse[JsonApiResource])
def read_organizations(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve organizations.
    """
    organizations = crud.organization.get_multi(db, skip=skip, limit=limit)
    resources = organization_serializer.serialize_many(organizations, db)
    
    return JsonApiResponse(
        data=resources,
        meta={"total": len(organizations)},
        links={
            "self": f"/api/v1/organizations?skip={skip}&limit={limit}",
            "first": "/api/v1/organizations?skip=0&limit={limit}",
        }
    )

@router.post("/", response_model=JsonApiResponse[JsonApiResource])
def create_organization(
    *,
    db: Session = Depends(deps.get_db),
    organization_in: OrganizationCreate,
) -> Any:
    """
    Create new organization.
    """
    organization = crud.organization.create(db=db, obj_in=organization_in)
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
    """
    Get organization by ID.
    """
    organization = crud.organization.get(db=db, id=organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
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
    organization_in: OrganizationCreate,
) -> Any:
    """
    Update an organization.
    """
    organization = crud.organization.get(db=db, id=organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    organization = crud.organization.update(db=db, db_obj=organization, obj_in=organization_in)
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
    """
    Delete an organization.
    """
    organization = crud.organization.get(db=db, id=organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    organization = crud.organization.remove(db=db, id=organization_id)
    resource = organization_serializer.serialize(organization, db)
    
    return JsonApiResponse(
        data=resource,
        links={"self": f"/api/v1/organizations/{organization_id}"}
    )
