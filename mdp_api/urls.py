from django.conf import settings
from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

from rest_framework.authtoken import views

from backent.api.views import router
from backent.api.views import CurrentUserView

from .views import json_signup, signup


urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^profile/$', CurrentUserView.as_view(), name='profile'),
    url(r'^token/', views.obtain_auth_token),
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^json_signup/$', json_signup, name='json_signup'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
