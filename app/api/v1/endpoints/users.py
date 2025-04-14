from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models
from app.api import deps
from app.schemas.schemas import UserCreate
from app.schemas.jsonapi import JsonApiResponse, JsonApiResource, JsonApiRequest
from app.serializers.user import user_serializer
from app.core.exceptions import ValidationException

router = APIRouter()

@router.get("/", response_model=JsonApiResponse[List[JsonApiResource]])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    resources = [user_serializer.serialize(user, db) for user in users]
    
    return JsonApiResponse(
        data=resources,
        meta={"total": len(users)},
        links={
            "self": f"/api/v1/users?skip={skip}&limit={limit}",
            "first": f"/api/v1/users?skip=0&limit={limit}",
        }
    )

@router.post("/", response_model=JsonApiResponse[JsonApiResource])
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    request: JsonApiRequest,
) -> Any:
    attrs = request.data.attributes
    user_in = UserCreate(
        first_name=attrs.first_name,
        last_name=attrs.last_name,
        email=attrs.email,
        password=attrs.password,
        owner=attrs.owner,
    )
    
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise ValidationException(
            detail="The user with this email already exists in the system."
        )
    
    user = crud.user.create(db=db, obj_in=user_in)
    resource = user_serializer.serialize(user, db)
    
    return JsonApiResponse(
        data=resource,
        links={"self": f"/api/v1/users/{user.id}"}
    )

@router.get("/{user_id}", response_model=JsonApiResponse[JsonApiResource])
def read_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
) -> Any:
    user = crud.user.get_or_404(db=db, id=user_id)
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
    request: JsonApiRequest,
) -> Any:
    user = crud.user.get_or_404(db=db, id=user_id)

    attrs = request.data.attributes
    user_in = UserCreate(
        first_name=attrs.first_name,
        last_name=attrs.last_name,
        email=attrs.email,
        password=attrs.password,
        owner=attrs.owner,
    )
    
    existing_user = crud.user.get_by_email(db, email=user_in.email)
    if existing_user and existing_user.id != user_id:
        raise ValidationException(
            detail="The user with this email already exists in the system."
        )
    
    user = crud.user.update(db=db, db_obj=user, obj_in=user_in)
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
    user = crud.user.remove(db=db, id=user_id)
    resource = user_serializer.serialize(user, db)
    
    return JsonApiResponse(
        data=resource,
        links={"self": f"/api/v1/users/{user_id}"}
    )
