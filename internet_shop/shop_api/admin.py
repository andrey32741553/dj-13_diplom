from django.contrib import admin
from django.contrib.admin import ModelAdmin, DateFieldListFilter

from shop_api.models import Product, Review, Order, Position, ProductCollections


class ReviewInline(admin.TabularInline):
    """Отзывы на странице фильма"""
    model = Review
    extra = 1
    readonly_fields = ("creator", "review_text", "rating")


class PositionInline(admin.TabularInline):
    """Позиции на странице заказов"""
    model = Position
    extra = 1
    list_display = ("product", "quantity")


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    """Продукты"""
    list_display = ("name", "description", "price", "created_at", "updated_at")
    inlines = [ReviewInline]


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    """Отзывы"""
    list_display = ("creator", "review_text", "rating", "product", "created_at", "updated_at")


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    """Заказы"""
    list_display = ("user", "status", "total", "count", "created_at", "updated_at")
    inlines = [PositionInline]
    list_filter = (
        ('created_at', DateFieldListFilter),
    )


@admin.register(ProductCollections)
class ProductCollectionsAdmin(ModelAdmin):
    """Подборки"""
    list_display = ('title', 'text', 'created_at', 'updated_at')
