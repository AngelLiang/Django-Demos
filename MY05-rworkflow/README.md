# 工作流程


## 备份配置和必要的数据

    $ python manage.py dumpdata rworkflow.workflow rworkflow.workflowcategory rworkflow.transitionapprovalmeta rworkflow.transitionmeta rworkflow.state organization hr auth.user -o fixtures\initdata.json

## 恢复配置和必要的数据

    $ python manage.py loaddata fixtures\initdata.json
