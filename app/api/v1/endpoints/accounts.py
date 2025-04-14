from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models
from app.api import deps
from app.schemas.schemas import AccountCreate
from app.schemas.jsonapi import JsonApiResponse, JsonApiResource, JsonApiRequest
from app.serializers.account import account_serializer

router = APIRouter()

@router.get("/", response_model=JsonApiResponse[List[JsonApiResource]])
def read_accounts(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    accounts = crud.account.get_multi(db, skip=skip, limit=limit)
    resources = [account_serializer.serialize(account, db) for account in accounts]
    
    return JsonApiResponse(
        data=resources,
        meta={"total": len(accounts)},
        links={
            "self": f"/api/v1/accounts?skip={skip}&limit={limit}",
            "first": f"/api/v1/accounts?skip=0&limit={limit}",
        }
    )

@router.post("/", response_model=JsonApiResponse[JsonApiResource])
def create_account(
    *,
    db: Session = Depends(deps.get_db),
    request: JsonApiRequest,
) -> Any:
    account_in = AccountCreate(name=request.data.attributes.name)
    account = crud.account.create(db=db, obj_in=account_in)
    resource = account_serializer.serialize(account, db)
    
    return JsonApiResponse(
        data=resource,
        links={"self": f"/api/v1/accounts/{account.id}"}
    )

@router.get("/{account_id}", response_model=JsonApiResponse[JsonApiResource])
def read_account(
    *,
    db: Session = Depends(deps.get_db),
    account_id: int,
) -> Any:
    account = crud.account.get_or_404(db=db, id=account_id)
    resource = account_serializer.serialize(account, db)
    
    return JsonApiResponse(
        data=resource,
        links={"self": f"/api/v1/accounts/{account_id}"}
    )

@router.put("/{account_id}", response_model=JsonApiResponse[JsonApiResource])
def update_account(
    *,
    db: Session = Depends(deps.get_db),
    account_id: int,
    request: JsonApiRequest,
) -> Any:
    account = crud.account.get_or_404(db=db, id=account_id)
    account_in = AccountCreate(name=request.data.attributes.name)
    account = crud.account.update(db=db, db_obj=account, obj_in=account_in)
    resource = account_serializer.serialize(account, db)
    
    return JsonApiResponse(
        data=resource,
        links={"self": f"/api/v1/accounts/{account_id}"}
    )

@router.delete("/{account_id}", response_model=JsonApiResponse[JsonApiResource])
def delete_account(
    *,
    db: Session = Depends(deps.get_db),
    account_id: int,
) -> Any:
    account = crud.account.remove(db=db, id=account_id)
    resource = account_serializer.serialize(account, db)
    
    return JsonApiResponse(
        data=resource,
        links={"self": f"/api/v1/accounts/{account_id}"}
    )
