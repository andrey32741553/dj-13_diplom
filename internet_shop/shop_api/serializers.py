from datetime import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User

from shop_api.models import Product, Review, Order, Position, ProductCollections, ProductListForCollection


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class ProductSerializer(serializers.ModelSerializer):
    """Serializer для списка продуктов."""

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'description')


class ReviewCreateSerializer(serializers.ModelSerializer):

    creator = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = ('creator', 'review_text', 'rating', 'product')

    def create(self, validated_data):
        """Метод для создания"""
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """ валидация количества отзывов и значения рейтинга """
        review_user = self.context["request"].user
        post_data = self.context["request"].data
        product_id = post_data.get('product')
        if int(post_data.get('rating')) < 1 or int(post_data.get('rating')) > 5:
            raise ValidationError({"Review": "Рейтинг должен быть от 1 до 5"})
        reviews_count = Review.objects.filter(creator=review_user).filter(product=product_id).count()
        if reviews_count >= 1:
            raise ValidationError({"Review": "Количество отзывов > 1"})
        return data


class ReviewUpdateSerializer(serializers.ModelSerializer):

    creator = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = ('creator', 'review_text', 'rating', 'product')

    def update(self, instance, validated_data):
        instance.review_text = validated_data.get('review_text', instance.review_text)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.updated_at = datetime.now()
        instance.save()
        return instance

    def validate(self, data):
        """ валидация количества отзывов и значения рейтинга """
        post_data = self.context["request"].data
        if int(post_data.get('rating')) < 1 or int(post_data.get('rating')) > 5:
            raise ValidationError({"Review": "Рейтинг должен быть от 1 до 5"})
        return data


class ReviewSerializer(serializers.ModelSerializer):

    creator = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    product = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):
    """Serializer для каждого продукта"""

    review = ReviewSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'review', 'created_at', 'updated_at')


class PositionSerializer(serializers.ModelSerializer):

    product = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )

    # order = serializers.SlugRelatedField(
    #     slug_field='user',
    #     read_only=True,
    # )

    class Meta:
        model = Position
        fields = ('product', 'order', 'quantity')


class PositionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Position
        fields = ('product', 'quantity')

    def create(self, validated_data):
        return Position.objects.create(**validated_data)


class OrderSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Order
        fields = ('id', 'user', 'status', 'total', 'created_at', 'updated_at')


class OrderUpdateSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Order
        fields = ('user', 'status', 'updated_at')

    def update(self, instance, validated_data):
        if self.context['request'].user.is_staff:
            instance.status = validated_data.get('status', instance.status)
            instance.updated_at = datetime.now()
            instance.save()
            return instance
        else:
            raise ValidationError({"Order": "Менять статус заказа может только админ"})


class OrderDetailSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    position = PositionSerializer(many=True)

    class Meta:
        model = Order
        fields = ('user', 'status', 'total', 'position', 'created_at', 'updated_at')


class OrderCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ()

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """ валидация количества заказов - не более одного для каждого пользователя"""
        order_user = self.context["request"].user
        orders_count = Order.objects.filter(user=order_user).count()
        if orders_count >= 1:
            raise ValidationError({"Order": "Количество заказов > 1. Дополните имеющийся заказ"})
        return data


class CollectionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCollections
        fields = ('id', 'title', 'text', 'created_at', 'updated_at')


class CollectionsCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCollections
        fields = ('title', 'text')

    def create(self, validated_data):
        return ProductCollections.objects.create(**validated_data)


class ProductToCollectionSerializer(serializers.ModelSerializer):

    product = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )

    class Meta:
        model = ProductListForCollection
        fields = ('product',)


class AddProductToCollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductListForCollection
        fields = ('collection', 'product')

    def create(self, validated_data):
        return ProductListForCollection.objects.create(**validated_data)

    def validate(self, data):
        post_data = self.context["request"].data
        collection_id = post_data.get('collection')
        product_id = post_data.get('product')
        product_name = Product.objects.get(id=product_id)
        collection_items = ProductListForCollection.objects.filter(collection_id=collection_id)
        for item in collection_items:
            if str(product_name) == str(item):
                raise ValidationError({"ProductListForCollection": "Товар уже есть в списке"})
        return data


class CollectionsDetailSerializer(serializers.ModelSerializer):

    product_list = ProductToCollectionSerializer(many=True)

    class Meta:
        model = ProductCollections
        fields = ('id', 'title', 'text', 'product_list', 'created_at', 'updated_at')
