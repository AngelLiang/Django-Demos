from django.contrib.contenttypes.models import ContentType

from .base import BaseManager


class EatraParamManager(BaseManager):

    def filter(self, *args, **kwarg):
        content_object = kwarg.pop('content_object', None)
        if content_object:
            kwarg['content_type'] = ContentType.objects.get_for_model(content_object)
            kwarg['object_id'] = content_object.pk

        return super().filter(*args, **kwarg)

    def update_or_create(self, *args, **kwarg):
        content_object = kwarg.pop('content_object', None)
        if content_object:
            kwarg['content_type'] = ContentType.objects.get_for_model(content_object)
            kwarg['object_id'] = content_object.pk

        return super().update_or_create(*args, **kwarg)

    def create_by_meta(self, meta):
        return self.create(
            name=meta.name,
            memo=meta.memo,
            value_tp=meta.value_tp,
        )
