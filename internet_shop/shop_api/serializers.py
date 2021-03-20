from datetime import datetime

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from shop_api.models import Product, Review, Order, Position, ProductCollections


class ProductSerializer(serializers.ModelSerializer):
    """Serializer для списка продуктов."""

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'description')


class ReviewSerializer(serializers.ModelSerializer):
    """ Сериализатор создания отзыва """

    creator = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = ('id', 'creator', 'review_text', 'rating', 'product')

    def create(self, validated_data):
        """Метод для создания"""
        validated_data["creator"] = self.context["request"].user
        review_user = self.context["request"].user
        product_id = validated_data['product'].id
        reviews_count = Review.objects.filter(creator=review_user).filter(product=product_id).count()
        if reviews_count >= 1:
            raise ValidationError({"Review": "Количество отзывов > 1"})
        else:
            return super().create(validated_data)

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


class ProductDetailSerializer(serializers.ModelSerializer):
    """Serializer для каждого продукта"""

    review = ReviewSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'review', 'created_at', 'updated_at')


class PositionSerializer(serializers.ModelSerializer):
    """ Сериализатор списка позиций """

    class Meta:
        model = Position
        fields = ("product", "quantity")


class OrderSerializer(serializers.ModelSerializer):
    """ Сериализатор списка заказов """

    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    products = PositionSerializer(many=True, source='position.all')

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('status',)

    def create(self, validated_data):
        validated_data['user'] = self.context["request"].user
        positions = validated_data.pop(
            'position')
        positions_objs = []
        validated_data['count'] = 0
        validated_data['total'] = 0
        order = super().create(validated_data)
        for position in positions.values():
            for item in position:
                price = Product.objects.get(id=item['product'].id).price
                validated_data['total'] += price * item['quantity']
                validated_data['count'] += item['quantity']
                positions_objs.append(Position(quantity=item['quantity'], product=item['product'], order=order))
        order.count = validated_data['count']
        order.total = validated_data['total']
        order.save()
        Position.objects.bulk_create(positions_objs)
        return order


class OrderDetailSerializer(serializers.ModelSerializer):
    """ Сериализатор конкретного заказа """

    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    position = PositionSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('user', 'status', 'total', 'count', 'position', 'created_at', 'updated_at')

    def update(self, instance, validated_data):
        """Метод для обновления + проверка на допустимость изменения"""
        if self.context['request'].user.is_authenticated:
            if validated_data['status'] == 'CANCELLED':
                instance.status = validated_data.get('status', instance.status)
                instance.updated_at = datetime.now()
                instance.save()
                return instance
            else:
                raise ValidationError({"Order": "Авторизованный пользователь может менять статус только на 'Отменён'"})
        elif self.context['request'].user.is_staff or self.context['request'].user.is_superuser:
            instance.status = validated_data.get('status', instance.status)
            instance.updated_at = datetime.now()
            instance.save()
            return instance
        else:
            raise ValidationError({"Order": "Менять статус заказа может только админ"})


class CollectionsSerializer(serializers.ModelSerializer):
    """ Сериализатор подборок товаров """

    class Meta:
        model = ProductCollections
        fields = ('id', 'title', 'text', 'products', 'created_at', 'updated_at')

    def create(self, validated_data):
        products = validated_data.pop('products')
        collection = ProductCollections.objects.create(**validated_data)
        collection.products.add(*products)
        return collection


class CollectionsDetailSerializer(serializers.ModelSerializer):
    """ Сериализатор конкретной подборки товаров """

    products = serializers.SerializerMethodField()

    def get_products(self, data):
        product_info = ProductCollections.objects.get(id=data.id).products.all()
        return ProductDetailSerializer(product_info, many=True).data

    class Meta:
        model = ProductCollections
        fields = ('id', 'title', 'text', 'products', 'created_at', 'updated_at')

    def update(self, instance, validated_data):
        if self.context['request'].user.is_staff:
            instance.title = validated_data.get('title', instance.title)
            instance.text = validated_data.get('text', instance.text)
            instance.updated_at = datetime.now()
            instance.save()
            return instance
        else:
            raise ValidationError({"Collections": "Менять информацию может только админ"})


class FavouritesCreateSerializer(serializers.ModelSerializer):
    """ Сериализатор создания списка избранных товаров """

    class Meta:
        model = User
        fields = ("products",)

    def create(self, validated_data):
        validated_data['username'] = self.context['request'].user
        products = validated_data.pop('products')
        user_info = User.objects.get(username=self.context['request'].user)
        for product in products:
            user_info.products.add(product.id)
        return user_info


class ProductSerializerForFavourites(serializers.ModelSerializer):
    """ Serializer для вывода списка избранных товаров """

    class Meta:
        model = Product
        fields = ('name',)


class UserSerializer(serializers.ModelSerializer):
    """Serializer для списка пользователей."""

    class Meta:
        model = User
        fields = ('id', 'username')


class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer для информации об избранных продуктах пользователя."""

    favourites = serializers.SerializerMethodField()

    def get_favourites(self, data):
        user_info = User.objects.get(id=self.context['request'].user.id)
        result = user_info.products.all()
        return ProductSerializerForFavourites(result, many=True).data

    order = OrderDetailSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('username', 'favourites', 'order')
