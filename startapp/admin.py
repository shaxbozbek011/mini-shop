from django.contrib import admin

from .models import Category, Product, OrderItem, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_active','category']
    list_filter = ['is_active','category']
    search_fields = ['name']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','user','status','created_at']
    list_filter = ['status']
    inlines = [OrderItemInline]


admin.site.register(Category)


