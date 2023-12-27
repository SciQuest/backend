from functools import wraps
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from users.models import Role


def protected(allowed_roles: list[Role]):
    def decorator(func):
        @wraps(func)
        def wrapper(request: Request, *args, **kwargs):
            if request.user.is_authenticated and request.user.role in allowed_roles:
                return func(request, *args, **kwargs)
            return Response(
                {"detail": "You don't have permission to access this resource."},
                status=status.HTTP_403_FORBIDDEN,
            )

        return wrapper

    return decorator
