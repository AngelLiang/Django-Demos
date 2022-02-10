FROM python:3.6-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY . .

# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pipenv -i https://mirrors.aliyun.com/pypi/simple/
RUN pipenv sync --system

# CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
CMD ["waitress-serve", "--listen=0.0.0.0:8000", "proj.wsgi:application"]
