from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(blank=True, null=True)
    has_newsletter = models.BooleanField(default=True)
    shop = models.ForeignKey('mdp_api_api.Shop', blank=True, null=True, related_name='users', on_delete=models.PROTECT)
