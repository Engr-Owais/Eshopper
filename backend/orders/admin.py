from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem, Favorite

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_items', 'total_price', 'updated_at')
    inlines = [CartItemInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'variant', 'price', 'quantity')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'status', 'payment_method', 'payment_completed', 'total_price', 'created_at')
    list_filter = ('status', 'payment_method', 'payment_completed')
    search_fields = ('user__username', 'user__email', 'full_name', 'email')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderItemInline]

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')
    list_filter = ('user',)
    search_fields = ('user__username', 'product__name')