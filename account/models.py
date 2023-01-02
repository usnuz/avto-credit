from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(upload_to='media/', blank=True, null=True)

    class Meta(AbstractUser.Meta):
        verbose_name = 'User'
        verbose_name_plural = 'Users'


