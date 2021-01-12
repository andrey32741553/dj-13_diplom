from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User

from shop_api.models import Product, Review


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

    creator = UserSerializer(
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
        if int(post_data.get('rating')) < 1 or int(post_data.get('rating')) > 5:
            raise ValidationError({"Review": "Рейтинг должен быть от 1 до 5"})
        reviews_count = Review.objects.filter(creator=review_user).count()
        if reviews_count > 1:
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

#
# class OrderSerializer(serializers.ModelSerializer):
#
#     user_id = serializers.SlugRelatedField(
#         slug_field='username',
#         read_only=True,
#     )
#
#     # position = serializers.SlugRelatedField(
#     #     slug_field='name',
#     #     read_only=True,
#     # )
#
#     class Meta:
#         model = Order
#         fields = '__all__'
#
#
# class OrderCreateSerializer(serializers.ModelSerializer):
#
#     user_id = serializers.SlugRelatedField(
#         slug_field='username',
#         read_only=True,
#     )
#
#     # position = serializers.SlugRelatedField(
#     #     slug_field='product',
#     #     read_only=True,
#     # )
#
#     class Meta:
#         model = Order
#         fields = ('id', 'user_id', 'position')
#
#     # def create(self, validated_data):
#     #     print(self.context["request"])
