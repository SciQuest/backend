from django.urls import path
from . import views


urlpatterns = [
    path("upload/", views.ArticleUploadView.as_view()),
    path("favorites/", views.FavoriteArticlesView.as_view()),
]
