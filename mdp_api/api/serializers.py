from django.contrib.auth import get_user_model

from rest_framework import serializers

from . import models


class CurrentUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'avatar',
            'first_name',
            'last_name',
        )


class ShopNameListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Shop
        fields = (
            'slug',
            'name',
        )


class ShopListSerializer(serializers.ModelSerializer):
    longitude = serializers.FloatField(source='coords.x')
    latitude = serializers.FloatField(source='coords.y')

    class Meta:
        model = models.Shop
        fields = (
            'name',
            'slug',
            'latitude',
            'longitude',
            'address',
            'zipcode',
            'city',
        )


class ShopDetailSerializer(serializers.ModelSerializer):
    longitude = serializers.FloatField(source='coords.x')
    latitude = serializers.FloatField(source='coords.y')

    class Meta:
        model = models.Shop
        fields = (
            'name',
            'slug',
            'description',
            'latitude',
            'longitude',
            'picture',
            'address',
            'zipcode',
            'city',
            'email',
            'phone',
        )
