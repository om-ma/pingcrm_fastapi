from app.serializers.base import ModelSerializer

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

contact_serializer = ContactSerializer()
