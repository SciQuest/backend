from django.urls import path
from . import views


urlpatterns = [
    path("articles/", views.ArticlesView.as_view()),
    path("articles/<int:article_id>/", views.ArticleView.as_view()),
    path("favorites/", views.FavoriteArticlesView.as_view()),
    path("favorites/<int:article_id>/", views.FavoriteArticleView.as_view()),
]
