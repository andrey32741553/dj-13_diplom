from django.contrib.auth.models import User
from django_filters import rest_framework as filters

from shop_api.models import Product, Review


class ProductFilter(filters.FilterSet):

    id = filters.ModelMultipleChoiceFilter(
        field_name='id',
        to_field_name='id',
        queryset=Product.objects.all(),
    )

    price = filters.NumberFilter()
    price__gt = filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = filters.NumberFilter(field_name='price', lookup_expr='lt')

    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')


class ReviewFilter(filters.FilterSet):

    product = filters.ModelChoiceFilter(queryset=Product.objects.all())

    class Meta:
        model = Review
        fields = ['product']

    creator = filters.ModelChoiceFilter(queryset=User.objects.all())

    class Meta:
        model = Review
        fields = ['creator']

    created_at = filters.DateFromToRangeFilter()

    class Meta:
        model = Review
        fields = ['created_at']
