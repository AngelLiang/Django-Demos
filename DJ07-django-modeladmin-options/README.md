# Django ModelAdmin Options Demo

准备工作

    # 数据库第一次迁移
    $ python manage.py migrate

    # 迁移 common 数据库
    $ python manage.py makemigrations common

    # 数据库第二次迁移
    $ python manage.py migrate

    # 创建管理员
    $ python manage.py createsuperuser

启动服务器

    $ python manage.py runserver

访问 http://127.0.0.1:8000/admin/ 即可

---

- https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#modeladmin-options
