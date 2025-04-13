from app.serializers.base import ModelSerializer

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

user_serializer = UserSerializer()
