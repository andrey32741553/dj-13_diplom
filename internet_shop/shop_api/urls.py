from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from shop_api.views import ProductViewSet, ReviewViewSet, OrderViewSet, PositionViewSet

urlpatterns = format_suffix_patterns([
    path('products/', ProductViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('products/<int:pk>/', ProductViewSet.as_view({'get': 'retrieve'})),
    path('product-reviews/', ReviewViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('orders/', OrderViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('orders/<int:pk>/', OrderViewSet.as_view({'get': 'retrieve'})),
    path('position/', PositionViewSet.as_view({'post': 'create'}))
])
