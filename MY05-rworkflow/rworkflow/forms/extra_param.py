from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from ..models import ExtraParamMeta, ExtraParam


class ExtraParamMetaForm(forms.ModelForm):
    class Meta:
        model = ExtraParamMeta
        fields = '__all__'


class ExtraParamForm(forms.ModelForm):
    class Meta:
        model = ExtraParam
        fields = '__all__'
