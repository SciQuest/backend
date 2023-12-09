from rest_framework.serializers import ModelSerializer
from . import models


class UserSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "role",
            "date_joined",
        )
        read_only_fields = ("id", "date_joined")
        extra_kwargs = {"password": {"write_only": True}}
