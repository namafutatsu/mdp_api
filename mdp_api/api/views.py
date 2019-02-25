from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.decorators import action
from rest_framework import generics
from rest_framework import routers
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import models
from .serializers import (
    CurrentUserSerializer,
)


class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = CurrentUserSerializer
    queryset = (
        get_user_model()
        .objects
        .all()
    )

    def retrieve(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(current_user)
        return Response(serializer.data)


router = routers.DefaultRouter()
