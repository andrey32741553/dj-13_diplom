import pytest
from django.urls import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_200_OK, HTTP_204_NO_CONTENT

from shop_api.models import Product


@pytest.mark.django_db
def test_create_product_by_authenticated_client(authenticated_client):
    """ Тест на невозможность создания товара пользователем """
    url = reverse("products-list")
    product = {"name": "Test", "price": 50, "description": "так себе яблоки"}
    response = authenticated_client.post(url, product)
    assert response.status_code == HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_create_product_by_admin(admin_client):
    """ Тест на создание товара админом """
    url = reverse("products-list")
    product = {"name": "Test", "price": 100, "description": "тест"}
    response = admin_client.post(url, product)
    assert response.status_code == HTTP_201_CREATED


@pytest.mark.django_db
def test_update_product_by_admin(admin_client, product_factory):
    """ Тест на изменение товара в списке """
    product = product_factory(_quantity=3)
    new_product_name = {"name": "новьё", "price": 150, "description": "подороже"}
    product_info = Product.objects.get(name=product[0])
    url = reverse("products-detail", args=(product_info.id,))
    resp = admin_client.put(url, data=new_product_name, format='json')
    new_product = Product.objects.get(name=new_product_name['name'])
    assert resp.status_code == HTTP_200_OK
    assert new_product.price == 150


@pytest.mark.django_db
def test_destroy_product_by_admin(admin_client, product_factory):
    """ Тест на удаление продукта из списка """
    product = product_factory(_quantity=3)
    product = Product.objects.get(name=product[0])
    url = reverse("products-detail", args=(product.id,))
    resp = admin_client.delete(url, format='json')
    assert resp.status_code == HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_products_list(client, product_factory):
    """ Тест на получение списка продуктов пользователем """
    product_factory(_quantity=3)
    url = reverse("products-list")
    resp = client.get(url)
    assert resp.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_products_retrieve(client, product_factory):
    """ Тест получения информации о конкретном продукте """
    product = product_factory(_quantity=3)
    product = Product.objects.get(name=product[0])
    url = reverse("products-detail", args=(product.id,))
    resp = client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert product.name == resp_json['name']


@pytest.mark.django_db
def test_price_filter(client, product_factory):
    """ Тест фильтра по цене """
    product_factory(_quantity=3)
    price_gt = 5
    price_lt = 110
    params = f'price__gt={price_gt}&price__lt={price_lt}'
    url = reverse("products-list") + '?' + params
    resp = client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    for item in resp_json:
        assert price_gt < float(item['price'])
        assert price_lt > float(item['price'])


@pytest.mark.django_db
def test_for_insistence_in_product_name(client, product_factory):
    """ Тест по содержимому в названии """
    product_factory(_quantity=3)
    name_part = 'гвоз'
    params = f'name={name_part}'
    url = reverse("products-list") + '?' + params
    resp = client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    for item in resp_json:
        assert name_part in item['name']


@pytest.mark.django_db
def test_for_insistence_in_description(product_factory, client):
    """ Тест по содержимому в описании """
    product_factory(_quantity=3)
    description_part = 'гвоз'
    params = f'description={description_part}'
    url = reverse("products-list") + '?' + params
    resp = client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    for item in resp_json:
        assert description_part in item['description']
