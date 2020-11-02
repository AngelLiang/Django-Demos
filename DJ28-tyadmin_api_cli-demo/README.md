# tyadmin_api_cli 示例项目

## 快速开始

    pipenv install
    python manage.py migrate
    python manage.py createsuperuser

    python manage.py runserver # 默认运行在8000端口

    # 新开一个控制台启动前端
    cd tyadmin
    npm install
    npm run start # 默认会运行在8001端口

最后访问：http://127.0.0.1:8001/xadmin/ 即可

## 使用 tyadmin_api_cli 扩展完整步骤

    pipenv install tyadmin-api-cli djangorestframework django-filter django-simple-captcha demjson
    python manage.py migrate
    python manage.py init_admin

    # 执行下面面命令后会自动生成 tyadmin 文件夹和 tyadmin_api 文件夹
    python manage.py gen_all


    # 修改 settings.py ， 导入 tyadmin_api


    # 再次进行数据库迁移
    python manage.py migrate
    # 创建超级管理员
    python manage.py createsuperuser
    python manage.py runserver # 默认运行在8000端口

    # 新开一个控制台
    cd tyadmin
    npm install
    npm run start # 默认会运行在8001端口

---

- https://github.com/mtianyan/tyadmin_api_cli

