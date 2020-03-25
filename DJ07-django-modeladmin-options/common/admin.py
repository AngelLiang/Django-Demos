from django.contrib import admin

# Register your models here.
from .models import Post, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    # site_title = '标签'
    list_display = ('name',)

    ####################################################################################

    def has_view_permission(request, obj=None):
        """
        https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.has_view_permission
        """
        return True

    def has_add_permission(self, request):
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

    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_max_show_all
    list_max_show_all = 200

    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_per_page
    list_per_page = 100

    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_select_related
    # list_select_related = ('user',)

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

    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.readonly_fields
    readonly_fields = ('create_date', 'create_time', 'update_datetime')

    # 分组显示
    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.fieldsets
    # fieldsets = (
    #     ('文章', {
    #         'fields': ('title', 'slug', 'content'),
    #         'classes': ('wide', 'extrapretty'),
    #     }),
    #     # 'field_options'
    # )

    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.radio_fields
    # admin.VERTICAL | admin.HORIZONTAL
    radio_fields = {'status': admin.HORIZONTAL}

    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.filter_horizontal
    filter_horizontal = ('tags',)  # 水平方式过滤器

    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.filter_vertical
    # filter_vertical = ('tags',)  # 垂直方式过滤器

    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.formfield_overrides
    # formfield_overrides = None

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

    # save_as_continue = False

    def save_model(self, request, obj, form, change):
        """保存事件
        :param request: HttpRequest
        :param obj: a model instance
        :param form: a ModelForm instance
        :param change: bool, whether it is adding or changing the object

        Overriding this method allows doing pre- or post-save operations.
        Call super().save_model() to save the object using Model.save().

        https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.save_model
        """
        print(f'change:{change}')
        obj.user = request.user
        return super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        """删除事件
        :param request:
        :param obj:

        https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.delete_model
        """
        return super().delete_model(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """
        https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.get_form
        """
        return super().get_form(request, obj, **kwargs)


admin.site.register(Post, PostAdmin)
