# Django2 使用 Celery5 示例工程

## 快速开始

    > pipenv install
    > pipenv shell

    # 迁移数据库
    > python manage.py migrate

    # 启动 celery
    > celery -A proj worker -l info

    # 加载beat数据
    > python manage.py loaddata -o .\fixtures\beat.json
    # 启动定时任务
    > celery -A proj beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

    # 创建管理员
    > python manage.py createsuperuser
    # 启动服务器
    > python manage.py runserver

## 执行一个任务

    > python manage.py shell
    >>> from tasktest import tasks
    >>> t = tasks.add.delay(8, 8)
