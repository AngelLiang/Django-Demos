"""软删除
第一次删除是软删除
第二次删除是硬删除
"""
from collections import Counter
from djtoolbox import softdeletion
from django.db import models
from django.db import router
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.utils import Collector, NestedObjects
# from django.db.models import signals
from django.utils import timezone

from .utils.save_signal_handle_model import SaveSignalHandlingModel
from .signals import pre_softdelete, post_softdelete


class DeleteCallback(object):
    def __init__(self, deleted_counter=None, using=None):
        self.deleted_counter = deleted_counter or Counter()
        self.using = using

    def delete_callback(self, obj):
        # 如果不是 SoftDeletionModelMixin 类则硬删除
        if not isinstance(obj, SoftDeletionModelMixin):
            obj.delete()
            return obj
        # 如果对象已经软删除，则进行硬删除
        if obj.is_deleted:
            obj.delete()
            return obj
        model = obj.__class__
        if not model._meta.auto_created:
            # 发送预软删除信号
            pre_softdelete.send(sender=model, instance=obj, using=self.using)

        obj._delete()
        # signals_to_disable： 禁止触发 pre_save 和 post_save 信号
        obj.save(update_fields=['is_deleted', 'deleted_at'], signals_to_disable=['pre_save', 'post_save'])
        self.deleted_counter[model._meta.label] += 1

        if not model._meta.auto_created:
            # 发送软删除结束信号
            post_softdelete.send(sender=model, instance=obj, using=self.using)
        return obj


class SoftDeletableQuerySet(QuerySet):
    def delete(self):
        """Delete the records in the current QuerySet."""
        assert self.query.can_filter(), \
            "Cannot use 'limit' or 'offset' with delete."

        if self._fields is not None:
            raise TypeError("Cannot call delete() after .values() or .values_list()")

        self._for_write = True
        del_query = self._chain()
        using = del_query.db

        dc = DeleteCallback(using=using)
        collector = NestedObjects(using=using)
        collector.collect(del_query)
        collector.nested(dc.delete_callback)
        return sum(dc.deleted_counter.values()), dict(dc.deleted_counter)


class AllSoftDeletedManager(models.Manager):
    _queryset_class = SoftDeletableQuerySet


class UnSoftDeletedManager(AllSoftDeletedManager):
    def get_queryset(self):
        """
        Return queryset limited to not deleted entries.
        """
        kwargs = {'model': self.model, 'using': self._db}
        if hasattr(self, '_hints'):
            kwargs['hints'] = self._hints

        qs = self._queryset_class(**kwargs)
        if hasattr(self.model, 'is_deleted'):
            return qs.filter(is_deleted=False)
        return qs


class SoftDeletedManager(AllSoftDeletedManager):
    def get_queryset(self):
        """
        Return queryset limited to not deleted entries.
        """
        kwargs = {'model': self.model, 'using': self._db}
        if hasattr(self, '_hints'):
            kwargs['hints'] = self._hints

        qs = self._queryset_class(**kwargs)
        if hasattr(self.model, 'is_deleted'):
            return qs.filter(is_deleted=True)
        return qs


class SoftDeletionModelMixin(SaveSignalHandlingModel):
    """
    注意：
    1）所有关联的对象都要有软删除的操作
    2）使用 unique 的字段要注意排除已删除的数据
    """
    class Meta:
        abstract = True

    # 软删除
    is_deleted = models.BooleanField(_('已删除'), default=False, editable=False, db_index=True)
    deleted_at = models.DateTimeField(_('删除时间'), null=True, blank=True, editable=False)

    objects = AllSoftDeletedManager()
    unsoftdelete_objects = UnSoftDeletedManager()
    softdelete_objects = SoftDeletedManager()

    def _delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()

    def _recover(self):
        self.is_deleted = False
        self.deleted_at = None

    def recover(self, using=None, keep_parents=False):
        """软删除数据恢复"""
        using = using or router.db_for_write(self.__class__, instance=self)
        collector = NestedObjects(using=using)
        collector.collect([self], keep_parents=keep_parents)

        def recover_callback(obj):
            # model = obj.__class__
            if obj.is_deleted:
                obj._recover()
                obj.save(update_fields=['is_deleted', 'deleted_at'])
            return obj

        collector.nested(recover_callback)

    def delete(self, using=None, soft=None, keep_parents=False, *args, **kwargs):
        """
        Soft delete object(set its ``is_deleted`` field to True).
        Actually delete object if setting ``soft`` to False.
        """
        using = using or router.db_for_write(self.__class__, instance=self)
        assert self.pk is not None, (
            "%s object can't be deleted because its %s attribute is set to None." %
            (self._meta.object_name, self._meta.pk.attname)
        )
        # 如果 soft 为 None，则取 self.is_deleted 反向值，
        #   self.is_deleted 为 False 时， soft=True，软删除
        #   self.is_deleted 为 True 时， soft=False，硬删除
        if soft is None:
            soft = not self.is_deleted
        if soft:
            dc = DeleteCallback(using=using)
            collector = NestedObjects(using=using)
            collector.collect([self], keep_parents=keep_parents)
            collector.nested(dc.delete_callback)
            return sum(dc.deleted_counter.values()), dict(dc.deleted_counter)
        else:
            return super().delete(using=using, *args, **kwargs)
