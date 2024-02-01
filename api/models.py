from django.db import models
from django.core.validators import FileExtensionValidator
from users.models import User


class Article(models.Model):
    pdf = models.FileField(
        upload_to="articles",
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
    )

    def delete(self, *args, **kwargs):
        self.pdf.delete(save=False)
        super().delete(*args, **kwargs)

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
