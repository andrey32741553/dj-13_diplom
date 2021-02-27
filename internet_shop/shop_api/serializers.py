from datetime import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from shop_api.models import Product, Review, Order, Position, Favourites, UserMethods, ProductCollections


class ProductSerializer(serializers.ModelSerializer):
    """Serializer для списка продуктов."""

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'description')


class ReviewCreateSerializer(serializers.ModelSerializer):
    """ Сериализатор создания отзыва """

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
    """ Сериализатор обновления отзыва """

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
        """ валидация значения рейтинга """
        post_data = self.context["request"].data
        if int(post_data.get('rating')) < 1 or int(post_data.get('rating')) > 5:
            raise ValidationError({"Review": "Рейтинг должен быть от 1 до 5"})
        return data


class ReviewSerializer(serializers.ModelSerializer):
    """ Сериализатор списка отзывов """

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
    """ Сериализатор списка позиций """

    product = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )

    class Meta:
        model = Position
        fields = ('product', 'quantity')


class PositionCreateSerializer(serializers.ModelSerializer):
    """ Сериализатор создания позиций в заказе """

    class Meta:
        model = Position
        fields = ('product', 'quantity')

    def create(self, validated_data):
        order_user = self.context["request"].user
        order_id = Order.objects.get(user=order_user).id
        return Position.objects.create(product=validated_data['product'],
                                       order_id=order_id,
                                       quantity=validated_data['quantity'])

    def validate(self, data):
        order_user = self.context["request"].user
        order_id = Order.objects.get(user=order_user).id
        products = Position.objects.filter(order_id=order_id)
        post_data = self.context["request"].data
        product_id = post_data.get('product')
        for product in products:
            if int(product_id) == product.product.id:
                raise ValidationError({"Position": "Товар уже есть в списке"})
        return data


class OrderSerializer(serializers.ModelSerializer):
    """ Сериализатор списка заказов """

    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Order
        fields = ('id', 'user', 'status', 'total', 'created_at', 'updated_at')


class OrderUpdateSerializer(serializers.ModelSerializer):
    """ Сериализатор обновления заказа """

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
    """ Сериализатор конкретного заказа """

    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    position = PositionSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('user', 'status', 'total', 'position', 'created_at', 'updated_at')


class OrderCreateSerializer(serializers.ModelSerializer):
    """ Сериализатор создания заказа """

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
    """ Сериализатор списка подборок """

    class Meta:
        model = ProductCollections
        fields = ('id', 'title', 'text', 'created_at', 'updated_at')


class CollectionsCreateSerializer(serializers.ModelSerializer):
    """ Сериализатор создания подборок товаров """

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


class FavouritesSerializer(serializers.ModelSerializer):
    """ Сериализатор списка избранных товаров """

    product = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )

    class Meta:
        model = Favourites
        fields = ('product',)


class FavouritesCreateSerializer(serializers.ModelSerializer):
    """ Сериализатор создания списка избранных товаров """

    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Favourites
        fields = ("product", "user")

    def create(self, validated_data):
        user = self.context["request"].user
        user_id = UserMethods.objects.get(username=user).id
        return Favourites.objects.create(product=validated_data['product'],
                                         user_id=user_id)

    """ Проверка на наличие товара в списке избранных """
    def validate(self, data):
        post_data = self.context["request"].data
        user_id = self.context['request'].user.id
        product_id = post_data.get('product')
        product_name = Product.objects.get(id=product_id)
        favourites_items = Favourites.objects.filter(user_id=user_id)
        for item in favourites_items:
            if str(product_name) == str(item):
                raise ValidationError({"Favourites": "Товар уже есть в списке"})
        return data


class UserSerializer(serializers.ModelSerializer):
    """Serializer для списка пользователей."""

    class Meta:
        model = UserMethods
        fields = ('id', 'username')


class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer для информации об избранных продуктах пользователя."""

    favourites = FavouritesSerializer(many=True, read_only=True)
    order = OrderDetailSerializer(many=True, read_only=True)

    class Meta:
        model = UserMethods
        fields = ('username', 'favourites', 'order')
