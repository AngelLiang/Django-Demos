from waitress import serve
from proj.wsgi import application

serve(application, listen='127.0.0.1:8080')
