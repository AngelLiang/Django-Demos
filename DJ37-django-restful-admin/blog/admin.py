from django.contrib import admin


from django_restful_admin import admin as api_admin
from blog.models import Post, Category

api_admin.site.register(Post)
api_admin.site.register(Category)


admin.site.register(Post)
admin.site.register(Category)

# from django_restful_admin import BaseRestFulModelAdmin

# @api_admin.register(Category, Post)
# class MyCustomApiAdmin(BaseRestFulModelAdmin):
#     # authentication_classes = (CustomTokenAuthentication,)
#     permission_classes = [IsAuthenticated]
