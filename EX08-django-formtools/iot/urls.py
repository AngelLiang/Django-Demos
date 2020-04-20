from django.contrib import admin
from django.urls import path

from . import forms
from .previews import DeviceFormPreview
from .wizardviews import DeviceWizard, FORMS

urlpatterns = [
    path('admin/', admin.site.urls),
    path('device/preview/', DeviceFormPreview(forms.DeviceForm)),
    path('device/wizardview/',
         DeviceWizard.as_view(
             [forms.CategoryForm, forms.DeviceForm, forms.AttributeForm])
         ),
]
