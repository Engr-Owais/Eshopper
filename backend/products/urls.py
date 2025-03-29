from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, ProductViewSet, ProductImageViewSet,
    ProductVariantViewSet, ReviewViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'', ProductViewSet)
router.register(r'images', ProductImageViewSet)
router.register(r'variants', ProductVariantViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]