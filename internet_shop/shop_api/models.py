from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.datetime_safe import datetime
from rest_framework.exceptions import ValidationError


class OrderStatusChoices(models.TextChoices):
    """Статусы заказа"""

    NEW = "NEW", "Получен"
    IN_PROGRESS = "IN_PROGRESS", "Выполняется"
    DONE = "DONE", "Готов"


class ProductCollections(models.Model):

    title = models.CharField("Заголовок", max_length=50)
    text = models.TextField()
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    def __str__(self):
        return self.title

    def get_productlistforcollection(self):
        return self.productlistforcollection.all()

    class Meta:
        verbose_name = "Подборка"
        verbose_name_plural = "Подборки"


class Product(models.Model):

    name = models.CharField("Название", max_length=50)
    description = models.TextField("Описание", default='')
    price = models.DecimalField("Цена", default=0.00, max_digits=10, decimal_places=2)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)
    product_collection = models.ForeignKey(
        ProductCollections,
        verbose_name="Подборки",
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name="products")

    def __str__(self):
        return f'{self.name}'

    def get_review(self):
        return self.review.all()

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Order(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        related_name="order"
    )
    status = models.TextField(
        OrderStatusChoices.choices,
        default=OrderStatusChoices.NEW
    )
    count = models.PositiveIntegerField(default=0)
    total = models.FloatField(default=0.00)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    def __str__(self):
        return "User: {} has {} items in order. Their total is ${}".format(self.user, self.count, self.total)

    def get_position(self):
        return self.position.all()

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["created_at"]


class ProductListForCollection(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_list')
    collection = models.ForeignKey(ProductCollections, on_delete=models.CASCADE, related_name='product_list')

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = "Коллекция"
        verbose_name_plural = "Коллекции"
        unique_together = ('product', 'collection')


class Position(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='position')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='position')
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return "This entry contains {} {}(s).".format(self.quantity, self.product.name)

    class Meta:
        verbose_name = "Наименование"
        verbose_name_plural = "Наименования"


class Review(models.Model):

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
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
        return f'{self.creator}, {self.product}'

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


@receiver(post_save, sender=Position)
def update_order(sender, instance, **kwargs):
    user_order = Order.objects.filter(user=instance.order.user)
    line_price = instance.quantity * instance.product.price
    instance.order.total += line_price
    user_order.update(total=instance.order.total)
    instance.order.count += instance.quantity
    user_order.update(count=instance.order.count)
    instance.order.updated_at = datetime.now()
    user_order.update(updated_at=instance.order.updated_at)


def save(self, *args, **kwargs):
    self.revision += 1
    return super(Position, self).save(*args, **kwargs)
