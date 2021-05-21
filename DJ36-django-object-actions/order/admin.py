from django.contrib import admin

from . import models
from django_object_actions import DjangoObjectActions


class CustomerAdmin(admin.ModelAdmin):
    pass


class ProductAdmin(admin.ModelAdmin):
    pass


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    extra = 1
    fields = ('product', 'quantity', 'price', 'amount',)
    readonly_fields = ('amount',)


class OrderAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ('__str__', 'order_date', 'title', 'amount')
    readonly_fields = ('amount',)
    inlines = (OrderItemInline,)

    # def save_model(self, request, obj, form, change):
    #     super().save_model(request, obj, form, change)
    #     obj.update_amount()

    def toolfunc(self, request, obj):
        pass
    toolfunc.label = "This will be the label of the button"  # optional
    toolfunc.short_description = "This will be the tooltip of the button"  # optional

    def make_published(modeladmin, request, queryset):
        pass
        # queryset.update(status='p')

    change_actions = ('toolfunc', )
    changelist_actions = ('make_published', )


admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Order, OrderAdmin)
