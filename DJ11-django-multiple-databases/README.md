# Django 使用多个数据库

## 准备工作

    # 初始化数据库
    python manage.py migrate --database=auth_db
    python manage.py migrate --database=primary
    python manage.py migrate --database=replica1
    python manage.py migrate --database=replica2

    # 创建管理员
    python manage.py createsuperuser --database auth_db

## 遗留问题

- django admin 首页无法查看，显示没有 auth_user 表

---

ref: https://docs.djangoproject.com/zh-hans/2.2/topics/db/multi-db/#an-example
