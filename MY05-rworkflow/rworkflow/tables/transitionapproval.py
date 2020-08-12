import django_tables2 as tables
from django.utils.translation import ugettext_lazy as _

from ..models import TransitionApproval


class TransitionApprovalTable(tables.Table):

    transaction_at = tables.Column(verbose_name=_('处理时间'))
    handler = tables.Column(verbose_name=_('处理者'), accessor='transactioner')
    result = tables.Column(verbose_name=_('处理结果'), accessor='transition__destination_state__name')
    memo = tables.Column(verbose_name=_('处理意见'))

    class Meta:
        model = TransitionApproval
        template_name = 'django_tables2/semantic.html'
        fields = ('transaction_at', 'handler', 'result', 'status', 'memo',)
        attrs = {'style': 'width:100%;'}
