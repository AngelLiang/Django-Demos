# 工作流程


## 备份配置和必要的数据

    $ python manage.py dumpdata rworkflow -o fixtures\initdata.json

## 恢复配置和必要的数据

    $ python manage.py loaddata fixtures\initdata.json
