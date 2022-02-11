# 使用docker部署django

## 快速开始

先 build 再 collectstatic， 最后 up，否则启动后静态文件可能不显示

    docker-compose build

    docker-compose exec dj python manage.py migrate
    docker-compose exec dj python manage.py collectstatic --noinput
    docker-compose exec dj python manage.py createsuperuser

    docker-compose up -d

## 参考

- https://learndjango.com/tutorials/django-docker-and-postgresql-tutorial
