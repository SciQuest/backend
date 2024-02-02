from django_elasticsearch_dsl import Document, Index, fields
from .utils.pdfs import extract_data
from . import models


articles_index = Index("sciquest_articles")
articles_index.settings(
    number_of_shards=1,
    number_of_replicas=0,
)


@articles_index.doc_type
class ArticleDocument(Document):
    title = fields.TextField()
    abstract = fields.TextField()
    authors = fields.TextField(
        analyzer="standard",
        multi=True,
        fields={
            "raw": fields.TextField(
                analyzer="keyword",
                multi=True,
            )
        },
    )
    institutions = fields.TextField(
        analyzer="standard",
        multi=True,
        fields={
            "raw": fields.TextField(
                analyzer="keyword",
                multi=True,
            )
        },
    )
    keywords = fields.TextField(
        analyzer="standard",
        multi=True,
        fields={
            "raw": fields.TextField(
                analyzer="keyword",
                multi=True,
            )
        },
    )
    text = fields.TextField()
    references = fields.TextField(multi=True)
    date = fields.DateField()

    class Django:
        model = models.Article
        fields = ["id", "pdf"]

    def prepare(self, instance):
        data = super(ArticleDocument, self).prepare(instance)
        data.update(extract_data(data["pdf"][1:]))
        return data
