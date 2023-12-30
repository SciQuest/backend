from rest_framework.serializers import ModelSerializer
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from . import models
from . import documents


class ArticleSerializer(ModelSerializer):
    class Meta:
        model = models.Article
        fields = ("id", "pdf")
        read_only_fields = ("id",)


class ArticleDocumentSerializer(DocumentSerializer):
    class Meta:
        model = models.Article
        document = documents.ArticleDocument

        fields = (
            "id",
            "title",
            "abstract",
            "authors",
            "institutions",
            "keywords",
            "text",
            "references",
            "pdf",
            "date",
        )

        read_only_fields = ("id",)
