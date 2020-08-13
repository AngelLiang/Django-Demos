from django import forms
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from ..models import TransitionMeta, State


class TransitionMetaForm(forms.ModelForm):
    source_state = forms.ModelChoiceField(label=_('初始状态'), queryset=State.objects, required=True)
    destination_state = forms.ModelChoiceField(label=_('目的状态'), queryset=State.objects, required=True)

    class Meta:
        model = TransitionMeta
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = self.instance
        if instance and instance.workflow_id:
            self.declared_fields['source_state'].queryset = instance.workflow.states
            self.declared_fields['destination_state'].queryset = instance.workflow.states
