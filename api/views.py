from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from users.utils.decorators import protected
from users.models import Role
from . import documents
from . import serializers


class ArticleUploadView(APIView):
    def post(self, request: Request):
        return self._post(request)

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


class FavoriteArticlesView(APIView):
    def get(self, request: Request):
        return self._get(request)

    @staticmethod
    @protected(allowed_roles=[Role.USER])
    def _get(request: Request):
        ids = list(request.user.profile.favorite_articles.values_list("id", flat=True))
        response = documents.ArticleDocument.search().filter("terms", id=ids).execute()
        articles = map(lambda hit: hit.to_dict(), response.hits)

        return Response(articles, status=status.HTTP_200_OK)
