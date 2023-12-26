from typing import Any
from django.db import models
from django.core.validators import FileExtensionValidator


class Article(models.Model):
    pdf = models.FileField(
        upload_to="articles",
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
    )

    def delete(
        self, using: Any = ..., keep_parents: bool = ...
    ) -> tuple[int, dict[str, int]]:
        self.pdf.delete()
        return super().delete(using, keep_parents)
