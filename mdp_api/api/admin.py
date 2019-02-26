from time import gmtime, strftime

from django.contrib import admin
from django.contrib.gis.db import models as gis_models
from django.db import models as django_models
from django.utils.html import mark_safe

from mapwidgets.widgets import GooglePointFieldWidget

from . import models


class GenericAdmin(admin.ModelAdmin):
    exclude = ('slug',)

    formfield_overrides = {
        gis_models.PointField: {"widget": GooglePointFieldWidget(attrs={'autocomplete': 'off'})},
    }


@admin.register(models.Shop)
class ShopAdmin(GenericAdmin):
    ordering = ('name',)

    readonly_fields = ["shop_image"]

    def shop_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url = obj.picture.url,
            width=obj.picture.width,
            height=obj.picture.height,
        )
    )


@admin.register(models.ShopNetwork)
class ShopNetworkAdmin(GenericAdmin):
    ordering = ('name',)


@admin.register(models.ShopRegion)
class ShopRegionAdmin(GenericAdmin):
    ordering = ('name',)
