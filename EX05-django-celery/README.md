# 给 Django 添加 Celery


## 准备工作

    需要安装 RabbitMQ


### 迁移 django celery 数据表

    $ python manage.py migrate django_celery_results


## 启动celery worker

    $ celery -A django_celery_demo worker -l info

---

- http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html

