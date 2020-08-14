from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from ..models import ExtraParamMeta, ExtraParam


class ExtraParamMetaForm(forms.ModelForm):
    class Meta:
        model = ExtraParamMeta
        fields = '__all__'


class ExtraParamForm(forms.ModelForm):

    paramvalue = forms.CharField(
        label=_('数值'), max_length=255, required=False,
    )

    class Meta:
        model = ExtraParam
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = self.instance
        if instance:
            value = instance.get_value()
            if value:
                self.declared_fields['paramvalue'].initial = value

    def save(self, *args, **kwargs):
        value = self.cleaned_data.get('paramvalue')
        self.instance.set_value(value)
        return super().save(*args, **kwargs)
