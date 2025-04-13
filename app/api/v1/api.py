from fastapi import APIRouter

from app.api.v1.endpoints import accounts, users, organizations, contacts

api_router = APIRouter()
api_router.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(organizations.router, prefix="/organizations", tags=["organizations"])
api_router.include_router(contacts.router, prefix="/contacts", tags=["contacts"])
