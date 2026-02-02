from django.contrib import admin
from .models import Customer, Products, Category, Order

# Register Customer model
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'city', 'country')
    search_fields = ('user__username', 'phone', 'city')
    list_filter = ('country', 'created_at')

# Register Products model
@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'stock', 'Category')
    search_fields = ('name', 'description')
    list_filter = ('Category', 'price')
    ordering = ('-id',)

# Register Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

# Register Order model
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_amount', 'status', 'created_at')
    search_fields = ('customer__user__username',)
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)
