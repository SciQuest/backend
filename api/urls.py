from django.urls import path
from . import views


urlpatterns = [
    path("articles/", views.ArticlesView.as_view(), name="articles"),
    path(
        "articles/search/",
        views.ArticleSearchView.as_view({"get": "list"}),
        name="search",
    ),
    path("articles/<int:article_id>/", views.ArticleView.as_view(), name="article"),
    path("favorites/", views.FavoriteArticlesView.as_view(), name="favorites"),
    path(
        "favorites/<int:article_id>/",
        views.FavoriteArticleView.as_view(),
        name="favorite",
    ),
]
