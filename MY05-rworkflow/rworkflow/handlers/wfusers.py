

def parent_position_handler(request, obj, node):
    """上级岗位

    :param request:
    :param obj:
    :param node:

    """

    from hr.models import Employee, Position

    # 获取该用户关联的职员
    emp_query = Employee.objects.filter(user=request.user)
    if emp_query.count() == 0:
        return None

    emp = emp_query.all()
    # 获取该职员的上级
    parent = [e.position.parent for e in emp if e.position and e.position.parent]

    # 获取上级职员
    query2 = Employee.objects.filter(position__in=parent).exclude(user=None)
    return [x.user for x in query2.all()]


wfusers_mapping = {
    'ParentPosition': parent_position_handler
}
