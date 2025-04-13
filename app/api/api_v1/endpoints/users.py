from typing import Any, List
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas.schemas import UserCreate
from app.schemas.jsonapi import JsonApiResponse, JsonApiResource
from app.serializers.serializers import user_serializer

router = APIRouter()

@router.get("/", response_model=JsonApiResponse[JsonApiResource])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve users.
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    resources = user_serializer.serialize_many(users, db)
    
    return JsonApiResponse(
        data=resources,
        meta={"total": len(users)},
        links={
            "self": f"/api/v1/users?skip={skip}&limit={limit}",
            "first": "/api/v1/users?skip=0&limit={limit}",
        }
    )

@router.post("/", response_model=JsonApiResponse[JsonApiResource])
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    resource = user_serializer.serialize(user, db)
    
    return JsonApiResponse(
        data=resource,
        links={"self": f"/api/v1/users/{user.id}"}
    )

@router.get("/{user_id}", response_model=JsonApiResponse[JsonApiResource])
def read_user(
    user_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get user by ID.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    resource = user_serializer.serialize(user, db)
    
    return JsonApiResponse(
        data=resource,
        links={"self": f"/api/v1/users/{user_id}"}
    )

@router.put("/{user_id}", response_model=JsonApiResponse[JsonApiResource])
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: UserCreate,
) -> Any:
    """
    Update a user.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    resource = user_serializer.serialize(user, db)
    
    return JsonApiResponse(
        data=resource,
        links={"self": f"/api/v1/users/{user_id}"}
    )

@router.delete("/{user_id}", response_model=JsonApiResponse[JsonApiResource])
def delete_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
) -> Any:
    """
    Delete a user.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = crud.user.remove(db=db, id=user_id)
    resource = user_serializer.serialize(user, db)
    
    return JsonApiResponse(
        data=resource,
        links={"self": f"/api/v1/users/{user_id}"}
    )
