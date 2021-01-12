from django.conf import settings
from django.db import models


class OrderStatusChoices(models.TextChoices):
    """Статусы заказа"""

    NEW = "NEW", "Получен"
    IN_PROGRESS = "IN_PROGRESS", "Выполняется"
    DONE = "DONE", "Готов"


# class Order(models.Model):
#
#     user_id = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         verbose_name="Пользователь",
#         on_delete=models.CASCADE
#     )
#
#     status = models.TextField(
#         OrderStatusChoices.choices,
#         default=OrderStatusChoices.NEW
#     )
#
#     # position = models.ForeignKey(
#     #         'Positions',
#     #         verbose_name='Наименование',
#     #         on_delete=models.CASCADE,
#     #         related_name='order'
#     #     )
#     total = models.DecimalField("Общая стоимость заказа", default=0.00, max_digits=10, decimal_places=2)
#     created_at = models.DateTimeField("Создано", auto_now_add=True)
#     updated_at = models.DateTimeField("Обновлено", auto_now=True)
#
#     def __str__(self):
#         return f'{self.id}, {self.user_id}, {self.status}, {self.total}'
#
#     def get_position(self):
#         return self.positions_set.all()
#
#     class Meta:
#         verbose_name = "Заказ"
#         verbose_name_plural = "Заказы"


# class Positions(models.Model):
#
#     count = models.PositiveSmallIntegerField(default=0)
#     order = models.ForeignKey(
#         Order,
#         verbose_name='Наименование продукта',
#         on_delete=models.CASCADE,
#         related_name='positions'
#     )
#
#     def get_product(self):
#         return self.product_set.all()


class Product(models.Model):

    name = models.CharField("Название", max_length=50)
    description = models.TextField("Описание", default='')
    price = models.DecimalField("Цена", default=0.00, max_digits=10, decimal_places=2)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)
    # position = models.ForeignKey(
    #     Positions,
    #     verbose_name='Наименование',
    #     on_delete=models.CASCADE,
    #     related_name='product'
    # )

    def __str__(self):
        return self.name

    def get_review(self):
        return self.review.all()

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


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

#
# class ProductCollections(models.Model):
#
#     title = models.CharField("Заголовок", max_length=50)
#     text = models.TextField()
#     product_collections = models.ManyToManyField(
#         Product,
#         verbose_name="Подборки",
#         related_name="collections"
#     )
#     created_at = models.DateTimeField("Создано", auto_now_add=True)
#     updated_at = models.DateTimeField("Обновлено", auto_now=True)
#
#     def __str__(self):
#         return self.title
#
#     class Meta:
#         verbose_name = "Подборка"
#         verbose_name_plural = "Подборки"
