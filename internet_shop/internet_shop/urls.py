"""internet_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from shop_api.views import ProductViewSet, ReviewViewSet, OrderViewSet, \
     UserViewSet, CollectionViewSet

router = routers.DefaultRouter()
router.register("products", ProductViewSet, basename="products")
router.register("product-reviews", ReviewViewSet, basename="product-reviews")
router.register("orders", OrderViewSet, basename="orders")
router.register("product-collections", CollectionViewSet, basename="product-collections")
router.register("user-info", UserViewSet, basename="user-info")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('shop_api.urls')),
    path('api/v1/', include(router.urls)),
]
