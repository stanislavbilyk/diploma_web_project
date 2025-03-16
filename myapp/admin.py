from django.contrib import admin
from .models import Product, Category, Brand, Color, OS, DeliveryService


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