from django.contrib import admin


# Register your models here.

# 添加数据模型
from .models import Question

admin.site.register(Question)
