from django.conf import settings
from django.urls import include, path, re_path
from django.views.static import serve

from django.contrib import admin
admin.autodiscover()

import rest_framework.authtoken.views
from rest_framework.documentation import include_docs_urls

from mdp_api.api import views

from . import views as account_views


urlpatterns = [
    # API views
    path('api/v0/shop-names/', views.ShopNameList.as_view()),
    path('api/v0/shops/', views.ShopList.as_view()),
    path('api/v0/shop/<str:slug>/', views.ShopDetail.as_view()),
    path('api/v0/docs/', include_docs_urls(title='Magasin de Producteurs', description="Description de l'API")),

    # Account related views
    path('account/profile/', views.CurrentUserView.as_view(), name='profile'),
    path('account/token/', rest_framework.authtoken.views.obtain_auth_token),
    path('account/signup/', account_views.signup, name='signup'),
    path('account/json_signup/', account_views.json_signup, name='json_signup'),

    # WWW views
    path('admin/', admin.site.urls, name='admin'),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
