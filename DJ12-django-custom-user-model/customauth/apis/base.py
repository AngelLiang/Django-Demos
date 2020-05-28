from rest_framework import viewsets

from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication,
)
from rest_framework.permissions import IsAuthenticated

from utils import JsonResponse


class BaseViewSet(viewsets.ModelViewSet):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication
    ]
    permission_classes = [IsAuthenticated]

    # def create(self, request, *args, **kwargs):
    #     # if request.headers.get('Content-Type') == 'text/plain':
    #     #     return super().create(request, *args, **kwargs)

    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return JsonResponse(data=serializer.data, headers=headers)

    # def list(self, request, *args, **kwargs):
    #     # if request.headers.get('Content-Type') == 'text/plain':
    #     #     return super().list(request, *args, **kwargs)

    #     queryset = self.filter_queryset(self.get_queryset())
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         data = {
    #             'items': serializer.data
    #         }
    #         return self.get_paginated_response(data)

    #     serializer = self.get_serializer(queryset, many=True)
    #     data = {
    #         'items': serializer.data
    #     }
    #     return JsonResponse(data=data)

    # def update(self, request, *args, **kwargs):
    #     """
    #     put /entity/{pk}/
    #     """
    #     # if request.headers.get('Content-Type') == 'text/plain':
    #     #     return super().update(request, *args, **kwargs)

    #     instance = self.get_object()
    #     serializer = self.get_serializer(
    #         instance, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return JsonResponse(data=serializer.data)

    # def destroy(self, request, *args, **kwargs):
    #     """
    #     delete /entity/{pk}/
    #     """
    #     # if request.headers.get('Content-Type') == 'text/plain':
    #     #     return super().destroy(request, *args, **kwargs)

    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return JsonResponse(message='数据删除成功')
