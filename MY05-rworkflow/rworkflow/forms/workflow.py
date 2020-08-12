from django import forms
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from ..core.workflowregistry import workflow_registry
from ..models import Workflow


def get_workflow_choices():
    def class_by_id(cid):
        return workflow_registry.class_index[cid]
    result = []
    for class_id, field_names in workflow_registry.workflows.items():
        cls = class_by_id(class_id)
        content_type = ContentType.objects.get_for_model(cls)
        for field_name in field_names:
            result.append(("%s %s" % (content_type.pk, field_name), "%s.%s - %s" %
                           (cls.__module__, cls.__name__, field_name)))
    return result


class WorkflowForm(forms.ModelForm):
    rstatus = forms.ChoiceField(label=_('工作流对象状态字段'), choices=[], required=True)

    class Meta:
        model = Workflow
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance", None)
        choices = get_workflow_choices()
        # if not choices:
        #     choices = []
        # choices.insert(0, ('', '-' * 8))
        self.declared_fields['rstatus'].choices = choices
        if instance and instance.pk:
            self.declared_fields['rstatus'].initial = "%s %s" % (instance.content_type.pk, instance.status_field)

        super().__init__(*args, **kwargs)

    def clean_rstatus(self):
        if self.cleaned_data.get('rstatus') == '' or ' ' not in self.cleaned_data.get('rstatus'):
            return None, None
        return self.cleaned_data.get('rstatus').split(' ')

    def save(self, *args, **kwargs):
        content_type_pk, field_name = self.cleaned_data.get('rstatus')
        instance = super().save(commit=False)
        if content_type_pk:
            instance.content_type = ContentType.objects.get(pk=content_type_pk)
            instance.status_field = field_name
        else:
            instance.content_type = None
            instance.status_field = field_name
        return super().save(*args, **kwargs)
