from django.contrib.auth.models import User
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from shop_api.filters import ProductFilter, ReviewFilter, OrderFilter
from shop_api.models import Product, Review, Order, ProductCollections

from shop_api.serializers import ProductSerializer, ProductDetailSerializer, \
    ReviewCreateSerializer, ReviewSerializer, OrderSerializer, OrderCreateSerializer, \
    PositionCreateSerializer, OrderDetailSerializer, \
    ReviewUpdateSerializer, OrderUpdateSerializer, \
    UserSerializer, UserDetailSerializer, \
    CollectionsSerializer, CollectionsCreateSerializer, \
    CollectionsDetailSerializer, FavouritesCreateSerializer


class ProductViewSet(ModelViewSet):
    """ViewSet для продуктов """

    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action in ["list", "create", "update"]:
            return ProductSerializer
        elif self.action == "retrieve":
            return ProductDetailSerializer

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "destroy"]:
            return [IsAdminUser()]
        return []


class ReviewViewSet(ModelViewSet):
    """ViewSet для отзывов """

    filter_backends = (DjangoFilterBackend,)
    filterset_class = ReviewFilter
    queryset = Review.objects.all()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ReviewSerializer
        elif self.action == "create":
            return ReviewCreateSerializer
        elif self.action == "update":
            return ReviewUpdateSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "retrieve", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return []

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        review_user = request.user
        instance = self.get_object()
        review_creator = instance.creator
        if review_user != review_creator:
            raise ValidationError({"Review": "Удалять можно только свои записи!"})
        return super().destroy(request, *args, **kwargs)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        review_user = request.user
        instance = self.get_object()
        review_creator = instance.creator
        if review_user != review_creator:
            raise ValidationError({"Review": "Обновлять можно только свои записи!"})
        return super().update(request, *args, **kwargs)


class OrderViewSet(ModelViewSet):
    """ViewSet для заказов """

    filter_backends = (DjangoFilterBackend,)
    filterset_class = OrderFilter
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return OrderSerializer
        elif self.action == "create":
            return OrderCreateSerializer

    def get_permissions(self):
        if self.action in ["list", "create", "destroy"]:
            return [IsAuthenticated()]
        elif self.action in ["list", "update"]:
            return [IsAdminUser()]
        return []

    @transaction.atomic
    def retrieve(self, request, *args, **kwargs):
        order_user = request.user
        instance = self.get_object()
        order_creator = instance.user
        if order_user != order_creator:
            raise ValidationError({"Order": "Просматривать можно только свои заказы!"})
        return super().retrieve(request, *args, **kwargs)


class OrderDetailViewSet(ModelViewSet):
    """ ViewSet для информации о заказе конкретного пользователя и добавления товаров в заказ """
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        elif self.action == "update":
            return OrderUpdateSerializer
        elif self.action == "create":
            return PositionCreateSerializer

    def get_permissions(self):
        if self.action in ["create", "destroy", "retrieve"]:
            return [IsAuthenticated()]
        elif self.action in ["update"]:
            return [IsAdminUser()]
        return []


class CollectionViewSet(ModelViewSet):
    """ViewSet для подборок """

    queryset = ProductCollections.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return CollectionsSerializer
        elif self.action == "create":
            return CollectionsCreateSerializer
        elif self.action in ["retrieve", "update"]:
            return CollectionsDetailSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "destroy"]:
            return [IsAdminUser()]
        return []


class UserViewSet(ModelViewSet):
    """ ViewSet для информации о пользователе """
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return UserSerializer
        elif self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return FavouritesCreateSerializer

    def get_permissions(self):
        if self.action in ["list", "create", "retrieve", "destroy"]:
            return [IsAuthenticated()]
        return []

    @transaction.atomic
    def retrieve(self, request, *args, **kwargs):
        request_user = self.request.user
        instance = self.get_object()
        request_creator = instance
        if request_user != request_creator:
            raise ValidationError({"Favourites": "Просматривать можно только свой список избранных товаров!"})
        return super().retrieve(request, *args, **kwargs)
