from django.utils.translation import gettext_lazy as _
from import_export.fields import Field
from import_export import resources, widgets

from ..models import Dictionary


class DictionaryResource(resources.ModelResource):

    class Meta:
        model = Dictionary
        fields = '__all__'
