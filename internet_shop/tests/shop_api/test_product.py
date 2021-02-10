from django.urls import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_200_OK, HTTP_204_NO_CONTENT

from shop_api.models import Product


def test_create_product_by_authenticated_client(client, django_user_model):
    """ Тест на невозможность создания товара пользователем """
    username = "foo"
    password = "bar"
    user = django_user_model.objects.create_user(username=username, password=password)
    client.force_login(user)
    url = reverse("products-list")
    product = {"name": "Test", "price": 50, "description": "так себе яблоки"}
    response = client.post(url, product)
    assert response.status_code == HTTP_403_FORBIDDEN


def test_create_product_by_admin(admin_client):
    """ Тест на создание товара админом """
    url = reverse("products-list")
    product = {"name": "Test", "price": 100, "description": "тест"}
    response = admin_client.post(url, product)
    assert response.status_code == HTTP_201_CREATED


def test_update_product_by_admin(admin_client):
    """ Тест на изменение товара в списке """
    """ Создание товара """
    url = reverse("products-list")
    product = {"name": "Test", "price": 100, "description": "тест"}
    response = admin_client.post(url, product)
    assert response.status_code == HTTP_201_CREATED
    """ Замена продукта в списке """
    new_product_name = {"name": "новьё", "price": 150, "description": "подороже"}
    product_info = Product.objects.get(name=product["name"])
    url = reverse("products-detail", args=(product_info.id,))
    resp = admin_client.put(url, data=new_product_name, content_type='application/json')
    new_product = Product.objects.get(name=new_product_name['name'])
    assert resp.status_code == HTTP_200_OK
    assert new_product.price == 150


def test_destroy_product_by_admin(admin_client):
    """ Тест на удаление продукта из списка """
    """ Создание товара """
    url = reverse("products-list")
    product = {"name": "Диван", "price": 50000, "description": "удобный"}
    response = admin_client.post(url, product)
    assert response.status_code == HTTP_201_CREATED
    """ Удаление товара """
    product = Product.objects.get(name=product["name"])
    url = reverse("products-detail", args=(product.id,))
    resp = admin_client.delete(url)
    assert resp.status_code == HTTP_204_NO_CONTENT


def test_products_list(client, admin_client):
    """ Тест на получение списка продуктов пользователем """
    """ Создание товара """
    url = reverse("products-list")
    product = {"name": "груши", "price": 50, "description": "получше яблок"}
    response = admin_client.post(url, product)
    assert response.status_code == HTTP_201_CREATED
    """ Получение списка """
    resp = client.get(url)
    assert resp.status_code == HTTP_200_OK


def test_products_retrieve(client, admin_client):
    """ Тест получения информации о конкретном продукте """
    """ Создание товара """
    url = reverse("products-list")
    product = {"name": "груши", "price": 100, "description": "получше яблок"}
    response = admin_client.post(url, product)
    assert response.status_code == HTTP_201_CREATED
    """ Получение информации о товаре """
    product = Product.objects.get(name=product["name"])
    url = reverse("products-detail", args=(product.id,))
    resp = client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert product.name == resp_json['name']


def test_price_filter(admin_client, client):
    """ Тест фильтра по цене """
    """ Создание товара """
    url = reverse("products-list")
    product = {"name": "гвозди", "price": 10, "description": "китайские"}
    product1 = {"name": "молоток", "price": 100, "description": "для забивания китайских гвоздей"}
    product2 = {"name": "доска", "price": 5, "description": "для китайских гвоздей"}
    response = admin_client.post(url, product)
    response1 = admin_client.post(url, product1)
    response2 = admin_client.post(url, product2)
    assert response.status_code == HTTP_201_CREATED
    assert response1.status_code == HTTP_201_CREATED
    assert response2.status_code == HTTP_201_CREATED
    """ Фильтр по цене """
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


def test_for_insistence_in_product_name(admin_client, client):
    """ Тест по содержимому в названии """
    """ Создание товара """
    url = reverse("products-list")
    product = {"name": "гвозди", "price": 10, "description": "китайские"}
    product1 = {"name": "молоток", "price": 100, "description": "для забивания китайских гвоздей"}
    product2 = {"name": "доска", "price": 5, "description": "для китайских гвоздей"}
    response = admin_client.post(url, product)
    response1 = admin_client.post(url, product1)
    response2 = admin_client.post(url, product2)
    assert response.status_code == HTTP_201_CREATED
    assert response1.status_code == HTTP_201_CREATED
    assert response2.status_code == HTTP_201_CREATED
    """ Тест по содержимому в названии """
    name_part = 'гвоз'
    params = f'name={name_part}'
    url = reverse("products-list") + '?' + params
    resp = client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    for item in resp_json:
        assert name_part in item['name']


def test_for_insistence_in_description(admin_client, client):
    """ Тест по содержимому в описании """
    """ Создание товара """
    url = reverse("products-list")
    product = {"name": "гвозди", "price": 10, "description": "китайские"}
    product1 = {"name": "молоток", "price": 100, "description": "для забивания китайских гвоздей"}
    product2 = {"name": "доска", "price": 5, "description": "для китайских гвоздей"}
    response = admin_client.post(url, product)
    response1 = admin_client.post(url, product1)
    response2 = admin_client.post(url, product2)
    assert response.status_code == HTTP_201_CREATED
    assert response1.status_code == HTTP_201_CREATED
    assert response2.status_code == HTTP_201_CREATED
    """ Фильтр по содержимому в описании """
    description_part = 'гвоз'
    params = f'description={description_part}'
    url = reverse("products-list") + '?' + params
    resp = client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    for item in resp_json:
        assert description_part in item['description']
