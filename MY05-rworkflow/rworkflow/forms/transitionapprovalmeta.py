from django import forms
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from ..models import TransitionApprovalMeta, TransitionMeta
from ..core.rule_parser import RuleParser, RuleEvaluationError


def _rule_help_text_html():
    from django.utils.html import format_html, format_html_join
    help_texts = [
        '格式为 ["操作符", ["操作符1", "参数1", "参数2", ...], ["操作符2", "参数3", "参数4", ...]]',
        '可以使用 "额外参数编号" 格式来代表额外参数的数值，例如："EX001"',
        '操作符包括： =, !=, >, >=, <, <=, and, or, not, in, str, int, +, -, *, / ',
    ]
    help_items = format_html_join('', '<li>{}</li>', ((help_text,) for help_text in help_texts))
    return format_html('<ul>{}</ul>', help_items) if help_items else ''


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

    # rule = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = TransitionApprovalMeta
        fields = '__all__'
        help_texts = {
            'rule': _rule_help_text_html
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance and instance.workflow:
            self.declared_fields['transition_meta'].queryset = instance.workflow.transition_metas
            self.declared_fields['parents'].queryset = instance.peers

        super().__init__(*args, **kwargs)

    def clean_rule(self):
        data = self.cleaned_data['rule']

        if data:
            try:
                RuleParser(data)
            except RuleEvaluationError as e:
                raise forms.ValidationError(e.args[0])
            except RuleEvaluationError as e:
                raise forms.ValidationError(e.args[0])
        return data
