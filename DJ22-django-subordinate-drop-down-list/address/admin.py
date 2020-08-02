from django.urls import path
from django.contrib import admin
from django.http import HttpResponse
from django.conf.urls import url

import json

from .models import Country, Province, Address


class CountryAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super().get_urls()
        return [
            url(r'(?P<obj_id>\d+)/provinces/', self.get_provinces),
        ] + urls

    def get_provinces(self, request, obj_id):
        obj = self.get_object(request, obj_id)
        if obj is None:
            # opts = self.opts
            # return self._get_obj_does_not_exist_redirect(request, opts, obj_id)
            return HttpResponse(json.dumps({}), content_type="application/json")

        # models = Province.objects.filter(country_id=obj_id)
        models = obj.provinces.all()
        result = [{'id': item.id, 'name': item.name} for item in models]
        return HttpResponse(json.dumps(result), content_type="application/json")


class ProvinceAdmin(admin.ModelAdmin):
    pass


class AddressAdmin(admin.ModelAdmin):
    pass


admin.site.register(Country, CountryAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(Address, AddressAdmin)
