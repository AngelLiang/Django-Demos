from django.contrib import admin


name = '后台系统管理'


class MyAdminSite(admin.AdminSite):
    site_header = name
    site_title = name
    index_title = name
