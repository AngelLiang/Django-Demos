from django import forms
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from ..models import TransitionApprovalMeta, TransitionMeta


class TransitionApprovalMetaForm(forms.ModelForm):
    name = forms.CharField(
        label=_('名称'), max_length=16, required=False,
        widget=forms.TextInput(attrs={'size': '40'}),
        help_text=_('该名称将显示在界面上')
    )

    transition_meta = forms.ModelChoiceField(
        label=_('流转元数据'), queryset=TransitionMeta.objects, required=True)
    parents = forms.ModelMultipleChoiceField(
        label=_('上级批准'), queryset=TransitionApprovalMeta.objects, required=False
    )

    class Meta:
        model = TransitionApprovalMeta
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance and instance.workflow:
            self.declared_fields['transition_meta'].queryset = instance.workflow.transition_metas
            self.declared_fields['parents'].queryset = instance.peers

        super().__init__(*args, **kwargs)
