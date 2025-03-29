from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem, Favorite
from products.serializers import ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the CartItem model.
    """
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    variant_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = CartItem
        fields = ('id', 'product', 'product_id', 'variant_id', 'quantity', 'total_price', 'created_at')
        read_only_fields = ('id', 'created_at')

class CartSerializer(serializers.ModelSerializer):
    """
    Serializer for the Cart model.
    """
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Cart
        fields = ('id', 'user', 'items', 'total_price', 'total_items', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the OrderItem model.
    """
    product_name = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_name', 'variant', 'price', 'quantity', 'total_price')
        read_only_fields = ('id', 'product_name', 'total_price')
    
    def get_product_name(self, obj):
        return obj.product.name

class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.
    """
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ('id', 'user', 'full_name', 'email', 'phone', 'address', 'city', 'state', 
                  'country', 'postal_code', 'status', 'payment_method', 'payment_completed', 
                  'total_price', 'items', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        """
        Create a new order with items from the user's cart.
        """
        user = self.context['request'].user
        cart = Cart.objects.get(user=user)
        
        if not cart.items.exists():
            raise serializers.ValidationError("Your cart is empty")
        
        # Create the order
        order = Order.objects.create(
            user=user,
            total_price=cart.total_price,
            **validated_data
        )
        
        # Create order items from cart items
        for cart_item in cart.items.all():
            variant_name = cart_item.variant.value if cart_item.variant else None
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                variant=variant_name,
                price=cart_item.product.discount_price if cart_item.product.discount_price else cart_item.product.price,
                quantity=cart_item.quantity
            )
        
        # Clear the cart
        cart.items.all().delete()
        
        return order

class FavoriteSerializer(serializers.ModelSerializer):
    """
    Serializer for the Favorite model.
    """
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Favorite
        fields = ('id', 'user', 'product', 'product_id', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')
    
    def create(self, validated_data):
        """
        Create a new favorite, setting the user from the request.
        """
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)