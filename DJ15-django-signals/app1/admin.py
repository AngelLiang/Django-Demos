from django.contrib import admin

# 添加数据模型
from .models import Question

admin.site.register(Question)
