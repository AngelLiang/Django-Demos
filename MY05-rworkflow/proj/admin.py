from django.contrib import admin
from django.conf import settings


proj_name = getattr(settings, 'PROJ_NAME') or '工作流程管理后台系统'


class MyAdminSite(admin.AdminSite):
    site_header = proj_name
    site_title = proj_name
    index_title = proj_name
