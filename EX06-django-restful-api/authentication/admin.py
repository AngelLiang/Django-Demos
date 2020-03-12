from django.contrib import admin

# https://www.django-rest-framework.org/api-guide/authentication/#with-django-admin
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']
