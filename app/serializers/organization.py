from app.serializers.base import ModelSerializer

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

organization_serializer = OrganizationSerializer()
