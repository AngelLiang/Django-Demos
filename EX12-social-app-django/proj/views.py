from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse


def social_auth_callback(request):
    # return render(request)
    print(request.GET.get('error_uri'))
    return HttpResponse('success')
