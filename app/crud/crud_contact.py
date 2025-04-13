from app.crud.base import CRUDBase
from app.models.contact import Contact
from app.schemas.schemas import ContactCreate, Contact as ContactSchema

class CRUDContact(CRUDBase[Contact, ContactCreate, ContactSchema]):
    pass

contact = CRUDContact(Contact)
