from django.contrib import admin

# Register your models here.
from .models import Post, Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


class PostAdmin(admin.ModelAdmin):

    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display
    list_display = ('title', 'slug', 'user', 'create_date',
                    'create_time', 'update_datetime')

    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display_links
    # list_display_links = ('title',)

    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_editable
    list_editable = ('slug',)

    # readonly_fields = ('view_count',)

    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter
    list_filter = ('create_date',)

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


admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
