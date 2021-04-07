from django.contrib import admin

from .models import Comment, Thing

admin.site.register(Comment)
admin.site.register(Thing)
