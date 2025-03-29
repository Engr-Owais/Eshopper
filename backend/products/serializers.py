from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductVariant, Review

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    """
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'description', 'image', 'parent', 'created_at')

class ProductImageSerializer(serializers.ModelSerializer):
    """
    Serializer for the ProductImage model.
    """
    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'alt_text', 'is_primary')

class ProductVariantSerializer(serializers.ModelSerializer):
    """
    Serializer for the ProductVariant model.
    """
    class Meta:
        model = ProductVariant
        fields = ('id', 'name', 'value')

class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.
    """
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = ('id', 'user', 'user_name', 'rating', 'comment', 'created_at')
        read_only_fields = ('user',)
    
    def get_user_name(self, obj):
        return obj.user.username
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    """
    category_name = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'description', 'price', 'discount_price', 
                  'category', 'category_name', 'stock', 'available', 'featured', 
                  'created_at', 'updated_at', 'images', 'variants', 'reviews')
    
    def get_category_name(self, obj):
        return obj.category.name