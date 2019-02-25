from django.contrib import admin
from django.contrib.admin.apps import AdminConfig


class mdp_apiAdminSite(admin.AdminSite):
    site_header = "CocoLarp admin"


class mdp_apiAdminConfig(AdminConfig):
    default_site = 'mdp_api.apps.mdp_apiAdminSite'
