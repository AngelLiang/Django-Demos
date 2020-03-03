from django.http import HttpResponse
from django.contrib import messages


def index(request):
    messages.add_message(request, messages.INFO, 'Hello world.')
    return HttpResponse('index')
