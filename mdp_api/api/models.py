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

from django_countries.fields import CountryField
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


class ShopNetwork(NameSlugMixin):
    description = models.TextField(null=True, blank=True)
    webpage = models.URLField(max_length=512, blank=True, null=True)


class ShopRegion(NameSlugMixin):
    coords = gis_models.PointField(geography=True)
    description = models.TextField()
    legacy_google = models.IntegerField(blank=True, null=True)


class FrenchDepartment(NameSlugMixin):
    code = models.CharField(max_length=3)
    region = models.ForeignKey(ShopRegion, on_delete=models.CASCADE)


class ShopQuerySet(models.QuerySet):

    def actives(self, **kwargs):
        return self.filter(
            is_active=True,
            **kwargs,
        )


class Shop(NameSlugMixin):
    is_active = models.BooleanField(default=True)
    description = models.TextField()
    highlights = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=10)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255, choices=enums.FRENCH_DEPARTMENTS)
    region = models.ForeignKey(ShopRegion, on_delete=models.PROTECT)
    country = CountryField(default='FR')
    coords = gis_models.PointField(geography=True)
    webpage = models.URLField(max_length=512, blank=True, null=True)
    network = models.ForeignKey(ShopNetwork, blank=True, null=True, on_delete=models.PROTECT)
    picture = models.ImageField(blank=True, null=True, upload_to='shop_images/')
    phone = PhoneNumberField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    organic_level = models.CharField(max_length=255, choices=enums.ORGANIC_LEVELS)

    objects = ShopQuerySet.as_manager()


class ShopComment(NameSlugMixin):
    shop = models.ForeignKey(Shop, related_name='comments', on_delete=models.CASCADE)
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
