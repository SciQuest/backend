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
            "last_login",
        )
        read_only_fields = ("id", "date_joined", "last_login")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        validated_data.pop("role", None)  # don't edit the role
        password = validated_data.pop("password", None)
        if password is not None:
            instance.set_password(password)
            instance.save()
        return super().update(instance, validated_data)
