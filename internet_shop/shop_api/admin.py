from django.contrib import admin
from django.contrib.admin import ModelAdmin

from shop_api.models import Product, Review


class ReviewInline(admin.TabularInline):
    """Отзывы на странице фильма"""
    model = Review
    extra = 1
    readonly_fields = ("creator", "review_text", "rating")


# class PositionInline(admin.TabularInline):
#     """Позиции на странице заказов"""
#     model = Positions
#     extra = 1
#     readonly_fields = ("count", "order")


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    """Продукты"""
    list_display = ("name", "description", "price", "created_at", "updated_at")
    inlines = [ReviewInline]


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    """Продукты"""
    list_display = ("creator", "review_text", "rating", "product", "created_at", "updated_at")


# @admin.register(Order)
# class OrderAdmin(ModelAdmin):
#     """Заказы"""
#     list_display = ("user_id", "status", "created_at", "updated_at")
#     readonly_fields = ("total",)
#     inlines = [PositionInline]
