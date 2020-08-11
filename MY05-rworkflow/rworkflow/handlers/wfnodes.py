from ..models import Node


def budget_gt_10000_handle(request, obj, node_config):
    """预算金额大于一万，由总经理审批"""
    budget = getattr(obj, 'budget', None)
    if budget and budget > 10000:
        return Node.objects.filter(id=7).all()


wfnodes_mapping = {
    # 项目预算金额大于一万
    'project.budget.gt.10000': budget_gt_10000_handle
}
