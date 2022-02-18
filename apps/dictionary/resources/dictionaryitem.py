from django.utils.translation import gettext_lazy as _
from import_export.fields import Field
from import_export import resources, widgets

from ..models import Dictionary, DictionaryItem
from .utils import AutoCreateForeginKeyWidget


class DictionaryItemResource(resources.ModelResource):

    master = Field(
        column_name=_('字典管理'),
        attribute='master',
        widget=AutoCreateForeginKeyWidget(Dictionary, field='code')
    )

    code = Field(
        column_name=_('编码'),
        attribute='code',
    )

    label = Field(
        column_name=_('标签'),
        attribute='label',
    )

    class Meta:
        model = DictionaryItem
        fields = '__all__'
        import_id_fields = ('master', 'code')
