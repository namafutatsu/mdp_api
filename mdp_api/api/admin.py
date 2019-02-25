from time import gmtime, strftime

from django.contrib import admin
from django.contrib.gis.db import models as gis_models
from django.db import models as django_models

from . import models


class GenericAdmin(admin.ModelAdmin):
    exclude = ('slug',)


@admin.register(models.Shop)
class ShopAdmin(GenericAdmin):
    ordering = ('name',)


@admin.register(models.ShopContact)
class ShopContactAdmin(GenericAdmin):
    ordering = ('name',)


@admin.register(models.ShopNetwork)
class ShopNetworkAdmin(GenericAdmin):
    ordering = ('name',)
