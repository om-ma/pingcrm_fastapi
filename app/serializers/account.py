from app.serializers.base import ModelSerializer

class AccountSerializer(ModelSerializer):
    def __init__(self):
        super().__init__(
            type_name="accounts",
            attributes=["name", "created_at", "updated_at"],
        )

account_serializer = AccountSerializer()
