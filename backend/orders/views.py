from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem, Order, OrderItem, Favorite
from .serializers import CartSerializer, CartItemSerializer, OrderSerializer, OrderItemSerializer, FavoriteSerializer
from products.models import Product, ProductVariant

class CartViewSet(viewsets.ModelViewSet):
    """
    API endpoint for shopping cart.
    """
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Return the cart for the current user.
        """
        return Cart.objects.filter(user=self.request.user)
    
    def get_object(self):
        """
        Get or create a cart for the current user.
        """
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart
    
    @action(detail=False, methods=['post'])
    def add_item(self, request):
        """
        Add an item to the cart.
        """
        cart = self.get_object()
        serializer = CartItemSerializer(data=request.data)
        
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            variant_id = serializer.validated_data.get('variant_id')
            quantity = serializer.validated_data.get('quantity', 1)
            
            product = get_object_or_404(Product, id=product_id)
            variant = None
            if variant_id:
                variant = get_object_or_404(ProductVariant, id=variant_id, product=product)
            
            # Check if the item already exists in the cart
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                variant=variant,
                defaults={'quantity': quantity}
            )
            
            # If the item already exists, update the quantity
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
            return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        """
        Remove an item from the cart.
        """
        cart = self.get_object()
        item_id = request.data.get('item_id')
        
        if not item_id:
            return Response({'error': 'Item ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            item = CartItem.objects.get(id=item_id, cart=cart)
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found in cart'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def update_item(self, request):
        """
        Update the quantity of an item in the cart.
        """
        cart = self.get_object()
        item_id = request.data.get('item_id')
        quantity = request.data.get('quantity')
        
        if not item_id or not quantity:
            return Response({'error': 'Item ID and quantity are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            item = CartItem.objects.get(id=item_id, cart=cart)
            
            if int(quantity) <= 0:
                item.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            
            item.quantity = int(quantity)
            item.save()
            
            return Response(CartItemSerializer(item).data)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found in cart'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def clear(self, request):
        """
        Clear all items from the cart.
        """
        cart = self.get_object()
        cart.items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint for orders.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Return orders for the current user.
        """
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)
    
    def perform_create(self, serializer):
        """
        Set the user when creating an order.
        """
        serializer.save(user=self.request.user)

class FavoriteViewSet(viewsets.ModelViewSet):
    """
    API endpoint for favorites.
    """
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Return favorites for the current user.
        """
        return Favorite.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """
        Set the user when creating a favorite.
        """
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def toggle(self, request):
        """
        Toggle a product as favorite.
        """
        product_id = request.data.get('product_id')
        
        if not product_id:
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        product = get_object_or_404(Product, id=product_id)
        
        # Check if the product is already a favorite
        favorite = Favorite.objects.filter(user=request.user, product=product).first()
        
        if favorite:
            # If it's already a favorite, remove it
            favorite.delete()
            return Response({'status': 'removed'}, status=status.HTTP_200_OK)
        else:
            # If it's not a favorite, add it
            Favorite.objects.create(user=request.user, product=product)
            return Response({'status': 'added'}, status=status.HTTP_201_CREATED)