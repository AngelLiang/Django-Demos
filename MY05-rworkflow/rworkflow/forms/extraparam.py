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
        instance = kwargs.get('instance', None)
        if instance:
            self.declared_fields['paramvalue'].required = instance.required
            self.declared_fields['paramvalue'].initial = instance.get_value()

        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        value = self.cleaned_data.get('paramvalue')
        self.instance.set_value(value)
        return super().save(*args, **kwargs)
