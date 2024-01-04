from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Role
from . import models


@receiver(post_save, sender=models.User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == Role.USER:
        models.Profile.objects.create(user=instance)


@receiver(post_save, sender=models.User)
def save_user_profile(sender, instance, **kwargs):
    if instance.role == Role.USER:
        instance.profile.save()
