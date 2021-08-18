"""软删除
第一次删除是软删除
第二次删除是硬删除
"""
from collections import Counter
from django.db import models
from django.db import router
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.utils import Collector, NestedObjects
from django.db.models import signals
from django.utils import timezone

from .utils.save_signal_handle_model import SaveSignalHandlingModel


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

        deleted_counter = Counter()
        def delete_callback(obj):
            if not isinstance(obj, SoftDeletionModelMixin):
                obj.delete()
                return obj
            model = obj.__class__
            if not model._meta.auto_created:
                # 发送预删除信号
                signals.pre_delete.send(sender=model, instance=obj, using=using)

            obj._delete()
            # signals_to_disable： 禁止触发 pre_save 和 post_save 信号
            obj.save(update_fields=['is_deleted', 'deleted_at'], signals_to_disable=['pre_save', 'post_save'])
            deleted_counter[model._meta.label] += 1
            
            if not model._meta.auto_created:
                # 发送删除结束信号
                signals.post_delete.send(sender=model, instance=obj, using=using)
            return obj

        collector = NestedObjects(using=using)
        collector.collect(del_query)
        to_delete_list = collector.nested(delete_callback)
        return sum(deleted_counter.values()), dict(deleted_counter)


class SoftDeletableManager(models.Manager):
    _queryset_class = SoftDeletableQuerySet

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


class SoftDeletedObjectManager(SoftDeletableManager):
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


class SoftDeletionModelMixin(SaveSignalHandlingModel, models.Model):
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

    objects = SoftDeletableManager()
    all_objects = models.Manager()
    # deleted_objects = SoftDeletedObjectManager()

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
            model = obj.__class__
            obj._recover()
            obj.save(update_fields=['is_deleted', 'deleted_at'])
            return obj

        to_recover_list = collector.nested(recover_callback)

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
            deleted_counter = Counter()
            collector = NestedObjects(using=using)
            collector.collect([self], keep_parents=keep_parents)

            def delete_callback(obj):
                if not isinstance(obj, SoftDeletionModelMixin):
                    obj.delete()
                    return obj
                model = obj.__class__
                if not model._meta.auto_created:
                    # 发送预删除信号
                    signals.pre_delete.send(sender=model, instance=obj, using=using)

                obj._delete()
                # signals_to_disable： 禁止触发 pre_save 和 post_save 信号
                obj.save(update_fields=['is_deleted', 'deleted_at'], signals_to_disable=['pre_save', 'post_save'])
                deleted_counter[model._meta.label] += 1
                
                if not model._meta.auto_created:
                    # 发送删除结束信号
                    signals.post_delete.send(sender=model, instance=obj, using=using)
                return obj

            to_delete_list = collector.nested(delete_callback)
            return sum(deleted_counter.values()), dict(deleted_counter)
        else:
            return super().delete(using=using, *args, **kwargs)

