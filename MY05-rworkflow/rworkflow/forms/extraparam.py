from django import forms
from django.forms import widgets
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from ..models import ExtraParamMeta, ExtraParam


value_tp_widget_mapping = {
    'bool': widgets.CheckboxInput(),
    'char': widgets.TextInput(),
    'text': widgets.TextInput(),
    'int': widgets.NumberInput(),
    'bigint': widgets.NumberInput(),
    'posint': widgets.NumberInput(),
    'date': widgets.DateInput(format='%Y-%m-%d'),
    'time': widgets.TimeInput(),
    'datetime': widgets.DateTimeInput(format='%Y-%m-%d %H:%M:%S'),
    'duration': widgets.TextInput(),
    'decimal': widgets.NumberInput(),
    # 附件暂时不能保存
    'file': widgets.ClearableFileInput(),
}


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
            widget = value_tp_widget_mapping.get(instance.value_tp)
            if widget:
                self.declared_fields['paramvalue'].widget = widget() if callable(widget) else widget

            value = instance.get_value()
            self.declared_fields['paramvalue'].initial = value
            # self.declared_fields['paramvalue'].help_text = instance.memo

        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        value = self.cleaned_data.get('paramvalue')
        self.instance.set_value(value)
        return super().save(*args, **kwargs)
