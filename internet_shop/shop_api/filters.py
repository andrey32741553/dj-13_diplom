from django.contrib.auth.models import User
from django_filters import rest_framework as filters

from shop_api.models import Product, Review, Order, OrderStatusChoices, Position


class ProductFilter(filters.FilterSet):

    # фильтр по цене (точной)
    price = filters.NumberFilter()

    # фильтр по диапазону цен
    price__gt = filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = filters.NumberFilter(field_name='price', lookup_expr='lt')

    # фильтр по части названия продукта
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    # фильтр по части текста описания
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')


class ReviewFilter(filters.FilterSet):

    # фильтр по ID продукта, по автору и дате создания
    product = filters.ModelChoiceFilter(queryset=Product.objects.all())
    creator = filters.ModelChoiceFilter(queryset=User.objects.all())
    created_at = filters.DateFromToRangeFilter()

    class Meta:
        model = Review
        fields = ['product', 'creator', 'created_at']


class OrderFilter(filters.FilterSet):

    # фильтр по статусу
    status = filters.MultipleChoiceFilter(
        choices=OrderStatusChoices.choices
    )

    # фильтр по диапазону общих сумм заказа
    total_price__gt = filters.NumberFilter(field_name='total', lookup_expr='gt')
    total_price__lt = filters.NumberFilter(field_name='total', lookup_expr='lt')

    # фильтр по товарам, по дате создания и обновления
    created_at = filters.DateFromToRangeFilter()
    updated_at = filters.DateFromToRangeFilter()
    position = filters.ModelChoiceFilter(queryset=Position.objects.all())

    class Meta:
        model = Order
        fields = ['created_at', 'updated_at', 'position']
