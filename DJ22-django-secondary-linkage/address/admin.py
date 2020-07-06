from django.urls import path
from django.contrib import admin
from django.http import HttpResponse
from django.conf.urls import url

import json

from .models import Country, Province, Address


class CountryAdmin(admin.ModelAdmin):
    pass


class ProvinceAdmin(admin.ModelAdmin):
    pass


class AddressAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super().get_urls()
        return urls + [
            # url(r'get_provinces/', self.get_provinces),
            url(r'get_provinces/(?P<obj_id>\d+)', self.get_provinces),
        ]

    def get_provinces(self, request, obj_id):
        models = Province.objects.filter(country_id=obj_id)
        result = [{'id': item.id, 'name': item.name} for item in models]
        return HttpResponse(json.dumps(result), content_type="application/json")


admin.site.register(Country, CountryAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(Address, AddressAdmin)
