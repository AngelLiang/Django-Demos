# from common.basemodel import BaseModel
# from common.basemodel import BaseModelWithOrgan

from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(_('创建时间'), null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), null=True, blank=True, auto_now=True)

    #################################################################
    # 使用用户名作为创建者和修改者的值
    #################################################################
    created_by = models.CharField(_('创建者'), max_length=80, default='', blank=True, db_index=True)
    updated_by = models.CharField(_('修改者'), max_length=80, default='', blank=True)
