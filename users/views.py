from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .utils.decorators import protected
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


class UserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request):
        serializer = serializers.UserSerializer(request.user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UsersView(APIView):
    def put(self, request: Request, user_id: int):
        return self._put(request, user_id)

    def delete(self, request: Request, user_id: int):
        return self._delete(request, user_id)

    @staticmethod
    @protected(allowed_roles=[models.Role.ADMIN])
    def _put(request: Request, user_id: int):
        moderator = get_object_or_404(
            models.User,
            pk=user_id,
            role=models.Role.MODERATOR,
        )

        serializer = serializers.UserSerializer(
            moderator,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @protected(allowed_roles=[models.Role.ADMIN])
    def _delete(request: Request, user_id: int):
        moderator = get_object_or_404(
            models.User,
            pk=user_id,
            role=models.Role.MODERATOR,
        )

        serializer = serializers.UserSerializer(moderator)
        moderator.delete()

        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
