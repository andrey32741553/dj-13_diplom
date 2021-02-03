from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from shop_api.filters import ProductFilter, ReviewFilter, OrderFilter
from shop_api.models import Product, Review, Order, Position, ProductCollections, ProductListForCollection

from shop_api.serializers import ProductListSerializer, ProductDetailSerializer, \
    ReviewCreateSerializer, ProductCreateSerializer, ReviewSerializer, OrderSerializer, OrderCreateSerializer, \
    PositionCreateSerializer, OrderDetailSerializer, CollectionsSerializer, CollectionsCreateSerializer, \
    AddProductToCollectionSerializer, CollectionsDetailSerializer, ProductUpdateSerializer


class ProductViewSet(ModelViewSet):
    """ViewSet для продуктов."""

    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        elif self.action == "retrieve":
            return ProductDetailSerializer
        elif self.action == "create":
            return ProductCreateSerializer
        elif self.action == "update":
            return ProductUpdateSerializer

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return []


class ReviewViewSet(ModelViewSet):

    filter_backends = (DjangoFilterBackend,)
    filterset_class = ReviewFilter
    queryset = Review.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return ReviewSerializer
        elif self.action == "create":
            return ReviewCreateSerializer

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create"]:
            return [IsAuthenticated()]
        return []

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        # print("Удаление внутри транзакции")
        # Получаем имя пользователя, который сделал запрос
        review_user = request.user
        # получаем имя пользователя, который создал сущность, которую нужно удалить
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

    filter_backends = (DjangoFilterBackend,)
    filterset_class = OrderFilter
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return OrderSerializer
        elif self.action == "create":
            return OrderCreateSerializer
        elif self.action == "retrieve":
            return OrderDetailSerializer
        elif self.action == "update":
            return OrderCreateSerializer

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "destroy"]:
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


class PositionViewSet(ModelViewSet):

    queryset = Position.objects.all()
    serializer_class = PositionCreateSerializer

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action == "create":
            return [IsAuthenticated()]
        return []


class CollectionViewSet(ModelViewSet):

    queryset = ProductCollections.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return CollectionsSerializer
        elif self.action == "create":
            return CollectionsCreateSerializer
        elif self.action == "retrieve":
            return CollectionsDetailSerializer

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action == "create":
            return [IsAdminUser()]
        return []


class AddProductToCollectionViewSet(ModelViewSet):

    queryset = ProductListForCollection.objects.all()
    serializer_class = AddProductToCollectionSerializer

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "destroy"]:
            return [IsAdminUser()]
        return []
