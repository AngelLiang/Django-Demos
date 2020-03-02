# Django 添加更多的视图

准备工作

    # 数据库第一次迁移
    # 主要是创建用户表等
    $ python manage.py migrate

    # 迁移 blog 数据库
    $ python manage.py makemigrations blog

    # 数据库第二次迁移
    $ python manage.py migrate

    # 创建 static 文件
    $ python manage.py collectstatic

    # 创建管理员
    $ python manage.py createsuperuser

启动服务器

    $ python manage.py runserver

访问 http://127.0.0.1:8000/admin/ 即可



---

https://docs.djangoproject.com/en/3.0/intro/tutorial07/
