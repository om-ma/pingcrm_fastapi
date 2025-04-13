from app.crud.base import CRUDBase
from app.models.organization import Organization
from app.schemas.schemas import OrganizationCreate, Organization as OrganizationSchema

class CRUDOrganization(CRUDBase[Organization, OrganizationCreate, OrganizationSchema]):
    pass

organization = CRUDOrganization(Organization)
