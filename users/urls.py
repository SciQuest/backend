from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views


urlpatterns = [
    path("user/", views.UserView.as_view(), name="user"),
    path("moderators/", views.ModeratorsView.as_view(), name="moderators"),
    path("moderators/<int:user_id>/", views.ModeratorView.as_view(), name="moderator"),
    path("register/", views.RegisterUserView.as_view(), name="register"),
    path("token/", views.CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
