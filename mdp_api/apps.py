from django.contrib import admin
from django.contrib.admin.apps import AdminConfig


class BackentAdminSite(admin.AdminSite):
    site_header = "CocoLarp admin"


class BackentAdminConfig(AdminConfig):
    default_site = 'backent.apps.BackentAdminSite'
