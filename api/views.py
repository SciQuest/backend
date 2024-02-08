from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_RANGE,
    LOOKUP_FILTER_TERM,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    MultiMatchSearchFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
)
from users.utils.decorators import protected
from users.models import Role
from . import models
from . import documents
from . import serializers


class ArticlesView(APIView):
    def get(self, request: Request):
        return self._get(request)

    def post(self, request: Request):
        return self._post(request)

    @staticmethod
    @protected(allowed_roles=[Role.USER, Role.MODERATOR, Role.ADMIN])
    def _get(request: Request):
        response = (
            documents.ArticleDocument.search()
            .sort({"date": {"order": "desc"}})
            .params(size=10000)
            .execute()
        )

        articles = map(lambda hit: hit.to_dict(), response.hits)

        return Response(articles, status=status.HTTP_200_OK)

    @staticmethod
    @protected(allowed_roles=[Role.ADMIN])
    def _post(request: Request):
        serializer = serializers.ArticleSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(
            documents.ArticleDocument.get(serializer.data["id"]).to_dict(),
            status=status.HTTP_201_CREATED,
        )


class ArticleView(APIView):
    def get(self, request: Request, article_id: int):
        return self._get(request, article_id)

    def put(self, request: Request, article_id: int):
        return self._put(request, article_id)

    def delete(self, request: Request, article_id: int):
        return self._delete(request, article_id)

    @staticmethod
    @protected(allowed_roles=[Role.USER, Role.MODERATOR, Role.ADMIN])
    def _get(request: Request, article_id: int):
        get_object_or_404(models.Article, pk=article_id)
        return Response(
            documents.ArticleDocument.get(article_id).to_dict(),
            status=status.HTTP_200_OK,
        )

    @staticmethod
    @protected(allowed_roles=[Role.MODERATOR])
    def _put(request: Request, article_id: int):
        get_object_or_404(models.Article, pk=article_id)
        document = documents.ArticleDocument.get(article_id)
        fields = set(serializers.ArticleDocumentSerializer.Meta.fields) - set(
            serializers.ArticleDocumentSerializer.Meta.read_only_fields
        )

        for key, value in request.data.items():
            if key not in fields:
                return Response(
                    {"detail": f"{key} is not a valid field to be updated"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            setattr(document, key, value)

        document.save()

        return Response(document.to_dict(), status=status.HTTP_200_OK)

    @staticmethod
    @protected(allowed_roles=[Role.MODERATOR])
    def _delete(request: Request, article_id: int):
        article = get_object_or_404(models.Article, pk=article_id)
        document = documents.ArticleDocument.get(article_id).to_dict()

        article.delete()

        return Response(document, status=status.HTTP_204_NO_CONTENT)


class ArticleSearchView(DocumentViewSet):
    document = documents.ArticleDocument
    serializer_class = serializers.ArticleDocumentSerializer

    filter_backends = [
        MultiMatchSearchFilterBackend,
        FilteringFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
    ]

    multi_match_search_fields = {
        "title": {"boost": 4},
        "keywords": {"boost": 3},
        "authors": {"boost": 2},
        "text": {"boost": 1},
    }

    multi_match_options = {
        "operator": "or",
    }

    filter_fields = {
        "keywords": {
            "field": "keywords.raw",
            "lookups": [LOOKUP_FILTER_TERM],
        },
        "authors": {
            "field": "authors.raw",
            "lookups": [LOOKUP_FILTER_TERM],
        },
        "institutions": {
            "field": "institutions.raw",
            "lookups": [LOOKUP_FILTER_TERM],
        },
        "date": {
            "field": "date",
            "lookups": [LOOKUP_FILTER_RANGE],
        },
    }

    ordering_fields = {"date": {"order": "desc"}}
    ordering = ("-date",)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.params(size=10000)


class FavoriteArticlesView(APIView):
    def get(self, request: Request):
        return self._get(request)

    @staticmethod
    @protected(allowed_roles=[Role.USER])
    def _get(request: Request):
        ids = list(request.user.profile.favorite_articles.values_list("id", flat=True))
        response = (
            documents.ArticleDocument.search()
            .filter("terms", id=ids)
            .sort({"date": {"order": "desc"}})
            .params(size=10000)
            .execute()
        )
        articles = map(lambda hit: hit.to_dict(), response.hits)

        return Response(articles, status=status.HTTP_200_OK)


class FavoriteArticleView(APIView):
    def post(self, request: Request, article_id: int):
        return self._post(request, article_id)

    def delete(self, request: Request, article_id: int):
        return self._delete(request, article_id)

    @staticmethod
    @protected(allowed_roles=[Role.USER])
    def _post(request: Request, article_id: int):
        article = get_object_or_404(models.Article, pk=article_id)
        profile = request.user.profile

        profile.favorite_articles.add(article)
        profile.save()

        return Response(
            documents.ArticleDocument.get(article_id).to_dict(),
            status=status.HTTP_201_CREATED,
        )

    @staticmethod
    @protected(allowed_roles=[Role.USER])
    def _delete(request: Request, article_id: int):
        article = get_object_or_404(models.Article, pk=article_id)
        profile = request.user.profile

        profile.favorite_articles.remove(article)
        profile.save()

        return Response(
            documents.ArticleDocument.get(article_id).to_dict(),
            status=status.HTTP_204_NO_CONTENT,
        )
