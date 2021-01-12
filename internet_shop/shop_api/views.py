from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from shop_api.filters import ProductFilter, ReviewFilter
from shop_api.models import Product, Review

from shop_api.serializers import ProductListSerializer, ProductDetailSerializer, \
    ReviewCreateSerializer, ProductCreateSerializer, ReviewSerializer


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
        # print("Удаление внутри транзакции")
        # Получаем имя пользователя, который сделал запрос
        review_user = request.user
        # получаем имя пользователя, который создал сущность, которую нужно удалить
        instance = self.get_object()
        review_creator = instance.creator

        if review_user != review_creator:
            raise ValidationError({"Review": "Обновлять можно только свои записи!"})

        return super().update(request, *args, **kwargs)


# class OrderViewSet(ModelViewSet):
#
#     queryset = Order.objects.all()
#
#     def get_serializer_class(self):
#         if self.action == "list":
#             return OrderSerializer
#         elif self.action == "create":
#             return OrderCreateSerializer
