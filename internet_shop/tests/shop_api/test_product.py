import pytest

from django.urls import reverse
from rest_framework.authtoken.admin import User
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_200_OK

from shop_api.models import Product, ProductCollections, Order


def test_create_product_by_authenticated_client(client, django_user_model):
    username = "foo"
    password = "bar"
    user = django_user_model.objects.create_user(username=username, password=password)
    client.force_login(user)
    url = reverse("products-list")
    product = {"name": "Test", "price": 50, "description": "так себе яблоки"}
    response = client.post(url, product)
    assert response.status_code == HTTP_403_FORBIDDEN


def test_create_product_by_admin(admin_client):
    url = reverse("products-list")
    product = {"name": "Test", "price": 100, "description": "тест"}
    response = admin_client.post(url, product)
    assert response.status_code == HTTP_201_CREATED


def test_create_review_by_authenticated_client(client, admin_client, django_user_model):
    url = reverse("products-list")
    product = {"name": "яблоки", "price": 50, "description": "так себе яблоки"}
    response = admin_client.post(url, product)
    assert response.status_code == HTTP_201_CREATED
    username = "foo"
    password = "bar"
    user = django_user_model.objects.create_user(username=username, password=password)
    client.force_login(user)
    url = reverse("reviews-list")
    product_info = Product.objects.get(name=product['name'])
    review = {'review_text': 'хорошая вещь', 'rating': 4, 'product': product_info.id}
    response = client.post(url, review)
    assert response.status_code == HTTP_201_CREATED


def test_create_order_and_positions_by_authenticated_client(client, admin_client, django_user_model):
    url = reverse("products-list")
    product = {"name": "гвозди", "price": 10, "description": "китайские"}
    response = admin_client.post(url, product)
    assert response.status_code == HTTP_201_CREATED
    username = "foo"
    password = "bar"
    user = django_user_model.objects.create_user(username=username, password=password)
    client.force_login(user)
    url = reverse("orders-list")
    name = User.objects.get(pk=user.pk)
    order = {"user": name.id, "status": "NEW"}
    response = client.post(url, order)
    assert response.status_code == HTTP_201_CREATED
    order_info = Order.objects.get(user=order['user'])
    product_info = Product.objects.get(name=product['name'])
    position = {'user': name.id, 'product': product_info.id, 'order': order_info.id, 'quantity': 5}
    response = client.post(url, position)
    assert response.status_code == HTTP_201_CREATED


def test_create_product_collections_by_admin(admin_client):
    url = reverse("products-list")
    product = {"name": "компьютер", "price": 10000, "description": "для офиса"}
    response = admin_client.post(url, product)
    assert response.status_code == HTTP_201_CREATED
    url = reverse("collections-list")
    collection = {"title": "для работы", "text": "надёжная техника для работы"}
    response = admin_client.post(url, collection)
    assert response.status_code == HTTP_201_CREATED
    collection_info = ProductCollections.objects.get(title=collection['title'])
    product_info = Product.objects.get(name=product['name'])
    collection_item = {'collection': collection_info.id, 'product': product_info.id,
                       "title": collection["title"], "text": collection["text"]}
    response = admin_client.post(url, collection_item)
    assert response.status_code == HTTP_201_CREATED
