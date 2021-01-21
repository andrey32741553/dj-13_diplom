from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User

from shop_api.models import Product, Review, Order, Position


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class ProductListSerializer(serializers.ModelSerializer):
    """Serializer для списка продуктов."""

    class Meta:
        model = Product
        fields = ('name', 'price', 'description')


class ProductCreateSerializer(serializers.ModelSerializer):
    """Serializer для списка продуктов."""

    class Meta:
        model = Product
        fields = ('name', 'price', 'description')


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
        """Метод для валидации. Вызывается при создании и обновлении."""
        # валидация количества отзывов и значения рейтинга
        review_user = self.context["request"].user
        post_data = self.context["request"].data
        product_id = post_data.get('product')
        if int(post_data.get('rating')) < 1 or int(post_data.get('rating')) > 5:
            raise ValidationError({"Review": "Рейтинг должен быть от 1 до 5"})
        reviews_count = Review.objects.filter(creator=review_user).filter(product=product_id).count()
        if reviews_count >= 1:
            raise ValidationError({"Review": "Количество отзывов > 1"})
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

    class Meta:
        model = Position
        fields = ('product', 'quantity')


class OrderSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Order
        fields = ('user', 'status', 'total', 'created_at', 'updated_at')


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

    # user = serializers.SlugRelatedField(
    #     slug_field='username',
    #     read_only=True,
    # )

    class Meta:
        model = Order
        fields = ('status',)

    def create(self, validated_data):
        """Метод для создания"""
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)


class PositionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Position
        fields = ('product', 'order', 'quantity')

    def create(self, validated_data):
        return Position.objects.create(**validated_data)
#
#     # def create(self, validated_data):
#     #     print(self.context["request"])

    # def create(self, validated_data):
    #     """Метод для создания"""
    #     validated_data["user_id"] = self.context["request"].user
    #     return super().create(validated_data)