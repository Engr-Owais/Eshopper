from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartViewSet, OrderViewSet, FavoriteViewSet

router = DefaultRouter()
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'favorites', FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('', include(router.urls)),
]