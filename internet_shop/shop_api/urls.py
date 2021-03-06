from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from shop_api.views import ProductViewSet, ReviewViewSet, OrderViewSet, \
     UserViewSet, CollectionViewSet

urlpatterns = format_suffix_patterns([
    path('products/', ProductViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('products/<int:pk>/', ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('product-reviews/', ReviewViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('product-reviews/<int:pk>/', ReviewViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('orders/', OrderViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('orders/<int:pk>/', OrderViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('product-collections/', CollectionViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('product-collections/<int:pk>/', CollectionViewSet.as_view({'get': 'retrieve', 'put': 'update',
                                                                     'delete': 'destroy'})),
    path('user-info/', UserViewSet.as_view({'get': 'list'})),
    path('user-info/<int:pk>/', UserViewSet.as_view({'get': 'retrieve', 'post': 'create'}))
])
