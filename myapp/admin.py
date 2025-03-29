from django.contrib import admin
from .models import Product, Category, Brand, Color, OS, DeliveryService
from django.contrib import admin
from django.utils.html import format_html
from .models import Refund

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity_on_storage')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(OS)
class OSAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(DeliveryService)
class OSAdmin(admin.ModelAdmin):
    list_display = ('name',)


class RefundAdmin(admin.ModelAdmin):
    list_display = ("purchase", "status", "time_of_refund", "refund_action")

    def refund_action(self, obj):
        if obj.status == "requested":
            return format_html('<a href="/admin/process-refund/{}/" class="button">Approve the refund</a>', obj.id)
        return "Обработан"

    refund_action.allow_tags = True

admin.site.register(Refund, RefundAdmin)