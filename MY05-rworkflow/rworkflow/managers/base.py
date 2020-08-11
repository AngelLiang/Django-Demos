

from django.db.models import QuerySet
from django.db.models.manager import BaseManager as _BaseManager


class BaseManager(_BaseManager.from_queryset(QuerySet)):
    pass
