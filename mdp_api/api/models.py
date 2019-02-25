import itertools
import textwrap

from django.conf import settings
from django.contrib.gis.db import models as gis_models
from django.core.cache import cache
from django.db import models
from django.db import IntegrityError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

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


class EventLike(models.Model):
    event = models.ForeignKey(
        'backent_api.Event',
        related_name='likes',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        'backent.User',
        related_name='likes',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return "Like from %s on %s" % (self.user, self.event)


class EventTag(models.Model):
    name = models.CharField(
        max_length=32,
        choices=enums.EVENT_TAG_CHOICES,
    )

    def __str__(self):
        return str(enums.EVENT_TAG_DICT[self.name])


class Language(models.Model):
    code = models.CharField(
        max_length=32,
        choices=enums.LANGUAGE_CHOICES,
    )

    def __str__(self):
        return str(enums.LANGUAGES_DICT[self.code])


class Event(NameSlugMixin):
    slug = models.SlugField(max_length=255)
    created_by = models.ForeignKey('backent.User', on_delete=models.PROTECT)
    organization = models.ForeignKey('backent_api.Organization', on_delete=models.PROTECT)
    location = models.ForeignKey('backent_api.Location', blank=True, null=True, on_delete=models.SET_NULL)
    summary = models.TextField()
    description = models.TextField()
    external_url = models.URLField(max_length=255)
    price = models.DecimalField(
        verbose_name=_(u"price (player)"),
        help_text="To be expressed in the event's currency",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    npc_price = models.DecimalField(
        verbose_name=_(u"price (NPC)"),
        help_text="To be expressed in the event's currency",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    start = models.DateTimeField(verbose_name=_(u"start"))
    event_format = models.CharField(
        max_length=32,
        choices=enums.EVENT_FORMAT_CHOICES,
        default=enums.EVENT_FORMAT_SHORT,
    )
    currency = models.CharField(
        max_length=32,
        choices=enums.CURRENCY_CHOICES,
        default=enums.CURRENCY_EUR,
    )
    facebook_event = models.URLField(max_length=255, blank=True, null=True)
    facebook_page = models.URLField(max_length=255, blank=True, null=True)
    facebook_group = models.URLField(max_length=255, blank=True, null=True)
    player_signup_page = models.URLField(max_length=255, blank=True, null=True)
    npc_signup_page = models.URLField(max_length=255, blank=True, null=True)

    tags = models.ManyToManyField(EventTag, related_name='events', blank=True)

    languages_spoken = models.ManyToManyField(Language, related_name='events', blank=True)

    class Meta:
        unique_together = (('name', 'start'),)


class Organization(NameSlugMixin):
    """Register an event's organizer. Except for its name, we don't have much info yet :/
    """
    pass


class Location(NameSlugMixin):
    address = models.CharField(max_length=512, blank=True, null=True,
        help_text="Leave blank if the location is still inaccurate",
    )
    coords = gis_models.PointField(geography=True)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


def force_save_all_models():
    # Useful to reset all the slugs and the eventual modified_at properties.
    for obj in Event.objects.all():
        obj.save()
    for obj in Organization.objects.all():
        obj.save()
    for obj in Location.objects.all():
        obj.save()
