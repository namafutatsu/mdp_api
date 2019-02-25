from django.contrib.auth import get_user_model

from rest_framework import serializers

from . import models


class LocationSerializer(serializers.ModelSerializer):
    longitude = serializers.FloatField(source='coords.x')
    latitude = serializers.FloatField(source='coords.y')

    class Meta:
        model = models.Location
        fields = (
            'slug',
            'name',
            'address',
            'latitude',
            'longitude',
        )


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Organization
        fields = (
            'slug',
            'name',
        )


class EventTagSerializer(serializers.RelatedField):

    def to_representation(self, value):
        return value.name


class LanguageSerializer(serializers.RelatedField):

    def to_representation(self, value):
        return value.code


class EventSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()
    location = LocationSerializer()
    tags = EventTagSerializer(many=True, read_only=True)
    languages = LanguageSerializer(many=True, read_only=True, source='languages_spoken')
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Event
        fields = (
            'pk',
            'slug',
            'name',
            'organization',
            'location',
            'summary',
            'description',
            'price',
            'npc_price',
            'currency',
            'start',
            'event_format',
            'external_url',
            'facebook_event',
            'facebook_page',
            'facebook_group',
            'player_signup_page',
            'npc_signup_page',
            'tags',
            'languages',
            'created_at',
            'updated_at',
            'like_count',
        )

    def get_like_count(self, obj):
        return obj.likes.count()


class LikedEventSerializer(serializers.RelatedField):

    def to_representation(self, value):
        return value.event.pk


class CurrentUserSerializer(serializers.ModelSerializer):

    events = LikedEventSerializer(many=True, read_only=True, source='likes')

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'avatar',
            'first_name',
            'last_name',
            'events',
        )
