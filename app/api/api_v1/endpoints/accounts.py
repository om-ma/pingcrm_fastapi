from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas.schemas import AccountCreate
from app.schemas.jsonapi import JsonApiResponse, JsonApiResource
from app.serializers.account import account_serializer

router = APIRouter()

@router.get("/", response_model=JsonApiResponse[JsonApiResource])
def read_accounts(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve accounts.
    """
    accounts = crud.account.get_multi(db, skip=skip, limit=limit)
    resources = account_serializer.serialize_many(accounts, db)
    
    return JsonApiResponse(
        data=resources,
        meta={"total": len(accounts)},
        links={
            "self": f"/api/v1/accounts?skip={skip}&limit={limit}",
            "first": "/api/v1/accounts?skip=0&limit={limit}",
        }
    )

@router.post("/", response_model=JsonApiResponse[JsonApiResource])
def create_account(
    *,
    db: Session = Depends(deps.get_db),
    account_in: AccountCreate,
) -> Any:
    """
    Create new account.
    """
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
    """
    Get account by ID.
    """
    account = crud.account.get(db=db, id=account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
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
    account_in: AccountCreate,
) -> Any:
    """
    Update an account.
    """
    account = crud.account.get(db=db, id=account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
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
    """
    Delete an account.
    """
    account = crud.account.get(db=db, id=account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    account = crud.account.remove(db=db, id=account_id)
    resource = account_serializer.serialize(account, db)
    
    return JsonApiResponse(
        data=resource,
        links={"self": f"/api/v1/accounts/{account_id}"}
    )
