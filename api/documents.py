from django_elasticsearch_dsl import Document, Index, fields
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
    authors = fields.TextField(multi=True)
    institutions = fields.TextField(multi=True)
    keywords = fields.TextField(multi=True)
    text = fields.TextField()
    references = fields.TextField(multi=True)

    class Django:
        model = models.Article
        fields = ["id", "pdf"]
