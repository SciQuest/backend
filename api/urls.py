from django.urls import path
from . import views

urlpatterns = [
    path("upload/", views.ArticleUploadView.as_view()),
]
