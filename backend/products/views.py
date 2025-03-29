from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product, ProductImage, ProductVariant, Review
from .serializers import (
    CategorySerializer, ProductSerializer, ProductImageSerializer,
    ProductVariantSerializer, ReviewSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
    
    @action(detail=True, methods=['get'])
    def products(self, request, slug=None):
        """
        Return all products in a category.
        """
        category = self.get_object()
        products = Product.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint for products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'available', 'featured']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at', 'name']
    
    @action(detail=True, methods=['post'])
    def add_review(self, request, slug=None):
        """
        Add a review to a product.
        """
        product = self.get_object()
        serializer = ReviewSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(product=product)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class ProductImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for product images.
    """
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        """
        Optionally filter by product.
        """
        queryset = ProductImage.objects.all()
        product_id = self.request.query_params.get('product', None)
        if product_id is not None:
            queryset = queryset.filter(product_id=product_id)
        return queryset

class ProductVariantViewSet(viewsets.ModelViewSet):
    """
    API endpoint for product variants.
    """
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        """
        Optionally filter by product.
        """
        queryset = ProductVariant.objects.all()
        product_id = self.request.query_params.get('product', None)
        if product_id is not None:
            queryset = queryset.filter(product_id=product_id)
        return queryset

class ReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint for reviews.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """
        Optionally filter by product or user.
        """
        queryset = Review.objects.all()
        product_id = self.request.query_params.get('product', None)
        user_id = self.request.query_params.get('user', None)
        
        if product_id is not None:
            queryset = queryset.filter(product_id=product_id)
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        
        return queryset
    
    def perform_create(self, serializer):
        """
        Set the user when creating a review.
        """
        serializer.save(user=self.request.user)