from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from users.utils.decorators import protected
from users.models import Role
from .utils.pdfs import extract_data
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
        article_document = documents.ArticleDocument.get(serializer.data["id"])
        document_data = extract_data(serializer.data["pdf"][1:])

        for key, value in document_data.items():
            setattr(article_document, key, value)
        article_document.save()

        return Response(article_document.to_dict(), status=status.HTTP_201_CREATED)
