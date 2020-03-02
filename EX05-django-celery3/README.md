# 给 Django 添加 Celery


## 准备工作

    需要安装 RabbitMQ


## 启动celery worker

    $ pipenv install
    $ pipenv shell
    $ celery -A django_celery_demo worker -l info

---

- http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html

