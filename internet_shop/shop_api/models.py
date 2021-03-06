from django.db import models
from django.contrib.auth.models import User


class OrderStatusChoices(models.TextChoices):
    """Статусы заказа"""

    NEW = "NEW", "Получен"
    IN_PROGRESS = "IN_PROGRESS", "Выполняется"
    DONE = "DONE", "Готов"
    CANCELLED = "CANCELLED", "Отменён"


class Product(models.Model):
    """ Модель товаров """

    name = models.CharField("Название", max_length=50)
    description = models.TextField("Описание", default='')
    price = models.FloatField("Цена", default=0.00)
    favourites = models.ManyToManyField(User, related_name='products')
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    def __str__(self):
        return self.name

    def get_review(self):
        return self.review.all()

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Order(models.Model):
    """ Модель заказов """

    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        related_name="order"
    )
    status = models.TextField(
        OrderStatusChoices.choices,
        default=OrderStatusChoices.NEW
    )
    products = models.ManyToManyField(Product, related_name='order', through='Position')
    count = models.PositiveIntegerField(editable=False)
    total = models.FloatField(editable=False)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    def __str__(self):
        return "User: {} has {} items in order. Their total is ${}".format(self.user, self.count, self.total)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["created_at"]


class Position(models.Model):
    """ Позиции товаров """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='position')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='position')
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return "This entry contains {} {}(s).".format(self.quantity, self.product.name)

    class Meta:
        verbose_name = "Наименование"
        verbose_name_plural = "Наименования"


class Review(models.Model):
    """ Отзывы """

    creator = models.ForeignKey(
        User,
        verbose_name="Автор",
        on_delete=models.CASCADE,
    )
    review_text = models.TextField("Отзыв")
    rating = models.PositiveSmallIntegerField("Оценка")
    product = models.ForeignKey(Product,
                                verbose_name='Наименование',
                                on_delete=models.CASCADE,
                                related_name='review')
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class ProductCollections(models.Model):
    """ Подборки товаров """

    title = models.CharField("Заголовок", max_length=50)
    text = models.TextField()
    products = models.ManyToManyField(Product, related_name='product_collections')
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Подборка"
        verbose_name_plural = "Подборки"
