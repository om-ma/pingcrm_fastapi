from app.serializers.base import ModelSerializer

class AccountSerializer(ModelSerializer):
    def __init__(self):
        super().__init__(
            type_name="accounts",
            attributes=["name", "created_at", "updated_at"],
        )

class UserSerializer(ModelSerializer):
    def __init__(self):
        super().__init__(
            type_name="users",
            attributes=[
                "first_name", "last_name", "email", "owner",
                "deleted_at", "created_at", "updated_at"
            ],
            relationships={
                "account": "accounts"
            }
        )

class OrganizationSerializer(ModelSerializer):
    def __init__(self):
        super().__init__(
            type_name="organizations",
            attributes=[
                "name", "email", "phone", "address", "city",
                "region", "country", "postal_code", "deleted_at",
                "created_at", "updated_at"
            ],
            relationships={
                "account": "accounts"
            }
        )

class ContactSerializer(ModelSerializer):
    def __init__(self):
        super().__init__(
            type_name="contacts",
            attributes=[
                "first_name", "last_name", "email", "phone",
                "address", "city", "region", "country",
                "postal_code", "deleted_at", "created_at", "updated_at"
            ],
            relationships={
                "account": "accounts",
                "organization": "organizations"
            }
        )

# Create instances for easy import
account_serializer = AccountSerializer()
user_serializer = UserSerializer()
organization_serializer = OrganizationSerializer()
contact_serializer = ContactSerializer()
