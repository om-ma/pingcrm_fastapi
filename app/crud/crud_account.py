from app.crud.base import CRUDBase
from app.models.account import Account
from app.schemas.schemas import AccountCreate, Account as AccountSchema

class CRUDAccount(CRUDBase[Account, AccountCreate, AccountSchema]):
    pass

account = CRUDAccount(Account)
