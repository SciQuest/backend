from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


class Admin(UserAdmin):
    model = models.User
    list_display = ["email", "first_name", "last_name", "role"]
    ordering = ["email"]


admin.site.register(models.User, Admin)
