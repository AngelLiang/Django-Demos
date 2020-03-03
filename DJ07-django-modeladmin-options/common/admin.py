from django.contrib import admin

# Register your models here.
from .models import Post, Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

    def has_add_permission(self, request):
        """
        https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.has_add_permission
        """
        return True

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True


class PostAdmin(admin.ModelAdmin):

    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display
    list_display = (
        'title', 'slug', 'status', 'user',
        'create_date', 'create_time',
        'update_datetime'
    )

    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display_links
    # list_display_links = ('title',)

    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_editable
    list_editable = ('status',)

    # readonly_fields = ('view_count',)

    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter
    list_filter = ('create_date', 'user__username')

    # Set date_hierarchy to the name of a DateField or DateTimeField in your model, and the change list page will include a date-based drilldown navigation by that field.
    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.date_hierarchy
    date_hierarchy = 'create_date'

    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.fields
    # fields = ('title', 'content')

    # This attribute, if given, should be a list of field names to exclude from the form.
    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.exclude
    exclude = ('money',)

    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.empty_value_display
    empty_value_display = 'unknown'

    # save_as_continue = False

    def save_model(self, request, obj, form, change):
        """
        :param change: bool, 是否是新建
        """
        print(f'change:{change}')
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def make_published(self, request, queryset):
        """
        https://docs.djangoproject.com/en/3.0/ref/contrib/admin/actions/
        """
        queryset.update(status='p')
        # for obj in queryset:
        #     do_something_with(obj)
    make_published.short_description = '标记所选的文章为发布状态'
    # Setting permissions for actions
    make_published.allowed_permissions = ('change',)
    actions = [make_published]  # 添加自定义的 action


admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
