from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from . import serializers
from . import models


class CustomTokenObtainPairView(TokenObtainPairView):
    class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
        @classmethod
        def get_token(cls, user):
            token = super().get_token(user)
            token["user_role"] = user.role
            return token

    serializer_class = CustomTokenObtainPairSerializer


class RegisterUserView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request: Request):
        if (
            not isinstance(request.user, AnonymousUser)
            and request.user.role == models.Role.ADMIN
        ):
            request.data["role"] = models.Role.MODERATOR
        else:
            request.data["role"] = models.Role.USER

        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
