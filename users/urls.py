from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views


urlpatterns = [
    path("register/", views.RegisterUserView.as_view()),
    path("token/", views.CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
