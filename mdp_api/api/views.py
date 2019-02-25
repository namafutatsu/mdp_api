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
    EventSerializer,
    LocationSerializer,
    OrganizationSerializer,
)


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EventSerializer

    def list(self, request, format=None):
        return super().list(request, format=format)

    def get_queryset(self):
        now = timezone.now()
        return models.Event.objects.filter(
            start__gte=now,
        ).prefetch_related(
            'tags',
            'languages_spoken',
        ).select_related(
            'location',
            'organization'
        )

    @action(methods=['post'], detail=True, permission_classes=(IsAuthenticated, ))
    def like(self, request, pk=None):
        event = self.get_object()
        like, created = models.EventLike.objects.get_or_create(
            event=event,
            user=request.user,
        )
        if not created:
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({}, status=status.HTTP_201_CREATED)


class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Location.objects.all()
    serializer_class = LocationSerializer


class OrganizationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Organization.objects.all()
    serializer_class = OrganizationSerializer


class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = CurrentUserSerializer
    queryset = (
        get_user_model()
        .objects
        .prefetch_related(
            'event__likes',
        )
    )

    def retrieve(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(current_user)
        return Response(serializer.data)


router = routers.DefaultRouter()
router.register(r'events', EventViewSet, base_name='event')
router.register(r'locations', LocationViewSet)
router.register(r'organizations', OrganizationViewSet)
