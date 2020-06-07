"""
Overview

Given a Form subclass that you define, this application takes care of the following workflow:

    1. Displays the form as HTML on a Web page.
    2. Validates the form data when it’s submitted via POST. a. If it’s valid, displays a preview page. b. If it’s not valid, redisplays the form with error messages.
    3. When the “confirmation” form is submitted from the preview page, calls a hook that you define – a done() method that gets passed the valid data.

"""

from django.http import HttpResponseRedirect

from formtools.preview import FormPreview
from .models import Device


class DeviceFormPreview(FormPreview):

    def done(self, request, cleaned_data):
        print(cleaned_data)
        device = Device.objects.create(**cleaned_data)
        print(device)
        # return HttpResponseRedirect(f'/admin/iot/device/')
        return HttpResponseRedirect(f'/admin/iot/device/{device.id}/change/')
