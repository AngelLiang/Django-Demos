# 使用docker部署django

## 快速开始

    docker-compose up -d --build

    docker-compose exec dj python manage.py migrate
    docker-compose exec dj python manage.py collectstatic --noinput
    docker-compose exec dj python manage.py createsuperuser

## 参考

- https://learndjango.com/tutorials/django-docker-and-postgresql-tutorial
