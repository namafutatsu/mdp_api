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

    # Migrate to departments
    fields = (
        'name', 'description', 'highlights', 'address', 'zipcode', 'city', 'department',
        'shop_region', 'country', 'coords', 'webpage', 'network', 'picture', 'shop_image',
        'phone', 'email', 'organic_level', 'is_active',
    )

    list_display = ('name', 'city', 'department', 'network', 'is_active')
    list_filter = ('department__region', 'network', 'is_active', 'organic_level',)
    search_fields = ('name', 'city', 'description', 'highlights',)

    autocomplete_fields = ('department', 'network')

    readonly_fields = ('shop_image', 'shop_region')

    def shop_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url = obj.picture.url,
            width=obj.picture.width,
            height=obj.picture.height,
        )
    )

    def shop_region(self, obj):
        return obj.department.region


@admin.register(models.ShopNetwork)
class ShopNetworkAdmin(GenericAdmin):
    ordering = ('name',)
    search_fields = ('name',)


@admin.register(models.ShopRegion)
class ShopRegionAdmin(GenericAdmin):
    ordering = ('name',)
    search_fields = ('name',)

    fields = ('name', 'description', 'coords')
    list_display = ('name',)
    search_fields = ('name', 'description', )

@admin.register(models.FrenchDepartment)
class FrenchDepartmentAdmin(GenericAdmin):
    ordering = ('name',)
    search_fields = ('name',)
    list_display = ('name', 'code', 'region',)
    list_filter = ('region',)
