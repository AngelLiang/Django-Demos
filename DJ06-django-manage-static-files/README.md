# Django 添加图片管理

## 准备工作

    # 数据库第一次迁移
    # 主要是创建用户表等
    $ python manage.py migrate

    # 迁移其他数据库
    $ python manage.py makemigrations common

    # 数据库第二次迁移
    $ python manage.py migrate

    # 创建管理员
    $ python manage.py createsuperuser

## 启动服务器

    $ python manage.py runserver

访问 http://127.0.0.1:8000/admin/ 即可

查看图片 http://localhost:8000/static/django.jpg


---

- https://docs.djangoproject.com/en/3.0/howto/static-files/
