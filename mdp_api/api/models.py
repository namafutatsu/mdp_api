import itertools
import textwrap

from django.conf import settings
from django.contrib.gis.db import models as gis_models
from django.core.cache import cache
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db import IntegrityError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from places.fields import PlacesField
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.authtoken.models import Token

from . import enums


class NameSlugMixin(models.Model):
    slug = models.SlugField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['slug']

    def __str__(self):
        return textwrap.shorten("{0.name}".format(self), 40)

    def save(self, *args, **kwargs):
        self.slug = orig = slugify(self.name)
        for x in itertools.count(1):
            conflicting_obj = self.__class__.objects.filter(slug=self.slug).order_by('pk').last()
            if conflicting_obj is None:
                break
            if conflicting_obj.pk == self.pk:
                break
            self.slug = '%s-%d' % (orig, x)
        super().save(*args, **kwargs)
        cache.clear()


class ShopNetwork(NameSlugMixin):
    pass


class ShopContact(NameSlugMixin):
    # Usually a shop contact and a producer contact
    kind = models.CharField(
        max_length=32,
        choices=enums.CONTACT_KINDS,
        default=enums.CONTACT_SHOP,
    )
    phone = PhoneNumberField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)


class Shop(NameSlugMixin):
    description = models.TextField()
    highlights = models.TextField(blank=True, null=True)
    location = PlacesField()
    webpage = models.URLField(max_length=512, blank=True, null=True)
    shop_contact = models.ForeignKey(ShopContact, on_delete=models.CASCADE)
    network = models.ForeignKey(ShopNetwork, on_delete=models.PROTECT)
    picture = models.ImageField(blank=True, null=True)

class ShopComment(NameSlugMixin):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    ranking = models.IntegerField(
        default=5,
        validators=[MaxValueValidator(5), MinValueValidator(1)],
    )


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
