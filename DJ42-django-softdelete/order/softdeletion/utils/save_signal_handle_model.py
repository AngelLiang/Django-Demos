from django.db import models, transaction, router
from django.db.models.signals import post_save, pre_save


class SaveSignalHandlingModel(models.Model):
    """
    An abstract base class model to pass a parameter ``signals_to_disable``
    to ``save`` method in order to disable signals
    """
    class Meta:
        abstract = True

    def save(self, signals_to_disable=None, *args, **kwargs):
        """
        Add an extra parameters to hold which signals to disable
        If empty, nothing will change
        """

        self.signals_to_disable = signals_to_disable or []

        super(SaveSignalHandlingModel, self).save(*args, **kwargs)

    def save_base(self, raw=False, force_insert=False,
                  force_update=False, using=None, update_fields=None):
        """
        Copied from base class for a minor change.
        This is an ugly overwriting but since Django's ``save_base`` method
        does not differ between versions 1.8 and 1.10,
        that way of implementing wouldn't harm the flow
        """
        using = using or router.db_for_write(self.__class__, instance=self)
        assert not (force_insert and (force_update or update_fields))
        assert update_fields is None or len(update_fields) > 0
        cls = origin = self.__class__

        if cls._meta.proxy:
            cls = cls._meta.concrete_model
        meta = cls._meta
        if not meta.auto_created and not 'pre_save' in self.signals_to_disable:
            pre_save.send(
                sender=origin, instance=self, raw=raw, using=using,
                update_fields=update_fields,
            )
        with transaction.atomic(using=using, savepoint=False):
            if not raw:
                self._save_parents(cls, using, update_fields)
            updated = self._save_table(raw, cls, force_insert, force_update, using, update_fields)

        self._state.db = using
        self._state.adding = False

        if not meta.auto_created and not 'post_save' in self.signals_to_disable:
            post_save.send(
                sender=origin, instance=self, created=(not updated),
                update_fields=update_fields, raw=raw, using=using,
            )

        # Empty the signals in case it might be used somewhere else in future
        self.signals_to_disable = []
