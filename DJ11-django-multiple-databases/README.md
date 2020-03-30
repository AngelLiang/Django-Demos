# Django使用多个数据库

## 准备工作

    # 初始化数据库
    python manage.py migrate --database=auth_db 

    # 创建管理员
    python manage.py createsuperuser --database auth_db
