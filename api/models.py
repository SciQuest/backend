from typing import Any
from django.db import models
from django.core.validators import FileExtensionValidator
from users.models import User


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

    def __str__(self) -> str:
        return str(self.pdf)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    favorite_articles = models.ManyToManyField(
        Article,
        related_name="favorited_by",
        blank=True,
    )

    def __str__(self) -> str:
        return str(self.user)
