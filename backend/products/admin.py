from django.contrib import admin
from .models import Category, Product, ProductImage, ProductVariant, Review

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('user', 'rating', 'comment', 'created_at')
    can_delete = False

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    list_filter = ('parent',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount_price', 'category', 'stock', 'available', 'featured')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('category', 'available', 'featured')
    search_fields = ('name', 'description')
    inlines = [ProductImageInline, ProductVariantInline, ReviewInline]

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text', 'is_primary')
    list_filter = ('is_primary',)
    search_fields = ('product__name', 'alt_text')

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'value')
    search_fields = ('product__name', 'name', 'value')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('product__name', 'user__username', 'comment')
    readonly_fields = ('created_at',)