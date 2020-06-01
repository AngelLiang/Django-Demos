from django.contrib import admin
from mptt.admin import MPTTModelAdmin

# from customauth import models
from django.contrib.auth import get_user_model
User = get_user_model()


class UserInline(admin.TabularInline):
    # model = settings.AUTH_USER_MODEL
    model = User
    can_delete = False
    fields = ['username', 'email', 'is_active', 'date_joined']

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False


class OrganizationAdmin(MPTTModelAdmin):
    list_display = ['name', 'code', 'leader', 'created_at']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

    fieldsets = (
        (None, {'fields':
                ('name', 'code', 'parent', 'leader',
                 'description',
                 'created_at', 'updated_at', 'created_by', 'updated_by',
                 )}
         ),
    )
    add_fieldsets = (
        (None, {'fields': ('name', 'code', 'parent', 'leader', 'description',)}
         ),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    inlines = [
        UserInline,
    ]

    def get_inlines(self, request, obj):
        if obj:
            return self.inlines
        return []

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
