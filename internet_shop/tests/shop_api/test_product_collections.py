from django.urls import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK

from shop_api.models import ProductCollections, Product


def test_create_product_collections_by_admin_and_list_by_user(admin_client, client):
    """ Тест создания подборок админом и вывода списка подборок пользователем """
    """ Создание подборок товаров админом"""
    url = reverse("products-list")
    product = {"name": "компьютер", "price": 10000, "description": "для офиса"}
    product1 = {"name": "принтер", "price": 5000, "description": "для офиса"}
    product2 = {"name": "ноутбук", "price": 100000, "description": "игровой"}
    product3 = {"name": "планшет", "price": 20000, "description": "игровой"}
    response = admin_client.post(url, product)
    response1 = admin_client.post(url, product1)
    response2 = admin_client.post(url, product2)
    response3 = admin_client.post(url, product3)
    assert response.status_code == HTTP_201_CREATED
    assert response1.status_code == HTTP_201_CREATED
    assert response2.status_code == HTTP_201_CREATED
    assert response3.status_code == HTTP_201_CREATED
    url = reverse("product-collections-list")
    collection = {"title": "для работы", "text": "надёжная техника для работы"}
    collection1 = {"title": "для развлечений", "text": "техника для развлечений"}
    response = admin_client.post(url, collection)
    response1 = admin_client.post(url, collection1)
    assert response.status_code == HTTP_201_CREATED
    assert response1.status_code == HTTP_201_CREATED
    collection_info = ProductCollections.objects.get(title=collection['title'])
    collection_info1 = ProductCollections.objects.get(title=collection1['title'])
    product_info = Product.objects.get(name=product['name'])
    product_info1 = Product.objects.get(name=product1['name'])
    product_info2 = Product.objects.get(name=product2['name'])
    product_info3 = Product.objects.get(name=product3['name'])
    collection_item = {'collection': collection_info.id, 'product': product_info.id}
    collection_item1 = {'collection': collection_info.id, 'product': product_info1.id}
    collection_item2 = {'collection': collection_info1.id, 'product': product_info2.id}
    collection_item3 = {'collection': collection_info1.id, 'product': product_info3.id}
    url = reverse("product-to-collection-list")
    response = admin_client.post(url, collection_item)
    response1 = admin_client.post(url, collection_item1)
    response2 = admin_client.post(url, collection_item2)
    response3 = admin_client.post(url, collection_item3)
    assert response.status_code == HTTP_201_CREATED
    assert response1.status_code == HTTP_201_CREATED
    assert response2.status_code == HTTP_201_CREATED
    assert response3.status_code == HTTP_201_CREATED
    """ Получение списка подборок пользователем """
    url = reverse("product-collections-list")
    resp = client.get(url)
    assert resp.status_code == HTTP_200_OK
