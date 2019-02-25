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
