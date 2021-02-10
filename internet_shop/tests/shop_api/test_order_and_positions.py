from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT

from shop_api.models import Order, Product, Position
import datetime as dt


def test_create_update_delete_order_and_positions_by_authenticated_client(client, admin_client, django_user_model):
    """ Тест на создание заказа; создание, обновление и удаление позиций заказа  """
    """ Создание списка товаров """
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
    """ Регистрация пользователя и создание заказа """
    username = "foo"
    password = "bar"
    user = django_user_model.objects.create_user(username=username, password=password)
    client.force_login(user)
    url = reverse("orders-list")
    name = User.objects.get(pk=user.pk)
    order = {"user": name.id, "status": "NEW"}
    resp = client.post(url, order)
    assert resp.status_code == HTTP_201_CREATED
    """ Создание позиций заказа пользователем """
    order_info = Order.objects.get(user=order['user'])
    url = reverse("positions-list")
    product_info = Product.objects.get(name=product['name'])
    product_info1 = Product.objects.get(name=product1['name'])
    product_info2 = Product.objects.get(name=product2['name'])
    position = {'user': name.id, 'product': product_info.id, 'order': order_info.id, 'quantity': 100}
    position1 = {'user': name.id, 'product': product_info1.id, 'order': order_info.id, 'quantity': 1}
    position2 = {'user': name.id, 'product': product_info2.id, 'order': order_info.id, 'quantity': 5}
    response = client.post(url, position)
    response1 = client.post(url, position1)
    response2 = client.post(url, position2)
    assert response.status_code == HTTP_201_CREATED
    assert response1.status_code == HTTP_201_CREATED
    assert response2.status_code == HTTP_201_CREATED
    """ Изменение количества товара в заказе """
    new_position = {'quantity': 10}
    position_info = Position.objects.get(product=position2["product"])
    url = reverse("positions-detail", args=(position_info.id,))
    resp = client.patch(url, data=new_position, content_type='application/json')
    new_position = Position.objects.get(product=position2["product"])
    assert resp.status_code == HTTP_200_OK
    assert new_position.quantity == 10
    """ Удаление позиции из заказа """
    position_info = Position.objects.get(product=position2["product"])
    url = reverse("positions-detail", args=(position_info.id,))
    resp = client.delete(url, position_info)
    assert resp.status_code == HTTP_204_NO_CONTENT


def test_get_list_of_orders(admin_client, client, django_user_model):
    """ Тест на вывод списка заказов """
    """ Создание списка товаров """
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
    """ Регистрация пользователя и создание заказа """
    username = "foo"
    password = "bar"
    user = django_user_model.objects.create_user(username=username, password=password)
    client.force_login(user)
    url = reverse("orders-list")
    name = User.objects.get(pk=user.pk)
    order = {"user": name.id, "status": "NEW"}
    resp = client.post(url, order)
    assert resp.status_code == HTTP_201_CREATED
    """ Вывод списка заказов админом """
    url = reverse("orders-list")
    resp = admin_client.get(url)
    assert resp.status_code == HTTP_200_OK
    """ Получение своего заказа пользователем"""
    order_info = Order.objects.get(user=order["user"])
    url = reverse("orders-detail", args=(order_info.id,))
    resp = client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert str(order_info.user) == resp_json['user']


def test_order_filter_by_total_price(admin_client, client, django_user_model):
    """ Тест фильтра по итоговой цене """
    """ Создание списка товаров """
    url = reverse("products-list")
    product = {"name": "гвозди", "price": 10, "description": "китайские"}
    product1 = {"name": "молоток", "price": 100, "description": "для забивания китайских гвоздей"}
    product2 = {"name": "доска", "price": 15, "description": "для китайских гвоздей"}
    response = admin_client.post(url, product)
    response1 = admin_client.post(url, product1)
    response2 = admin_client.post(url, product2)
    assert response.status_code == HTTP_201_CREATED
    assert response1.status_code == HTTP_201_CREATED
    assert response2.status_code == HTTP_201_CREATED
    """ Регистрация пользователя и создание заказа """
    username = "foo"
    password = "bar"
    user = django_user_model.objects.create_user(username=username, password=password)
    client.force_login(user)
    url = reverse("orders-list")
    name = User.objects.get(pk=user.pk)
    order = {"user": name.id, "status": "NEW"}
    resp = client.post(url, order)
    assert resp.status_code == HTTP_201_CREATED
    """ Создание позиций заказа пользователем """
    order_info = Order.objects.get(user=order['user'])
    url = reverse("positions-list")
    product_info = Product.objects.get(name=product['name'])
    product_info1 = Product.objects.get(name=product1['name'])
    product_info2 = Product.objects.get(name=product2['name'])
    position = {'user': name.id, 'product': product_info.id, 'order': order_info.id, 'quantity': 100}
    position1 = {'user': name.id, 'product': product_info1.id, 'order': order_info.id, 'quantity': 1}
    position2 = {'user': name.id, 'product': product_info2.id, 'order': order_info.id, 'quantity': 5}
    response = client.post(url, position)
    response1 = client.post(url, position1)
    response2 = client.post(url, position2)
    assert response.status_code == HTTP_201_CREATED
    assert response1.status_code == HTTP_201_CREATED
    assert response2.status_code == HTTP_201_CREATED
    """ Фильтр по итоговой цене заказа """
    order_info = Order.objects.get(user=order['user'])
    total_price__gt = 10
    total_price__lt = 1200
    params = f'total_price__gt={total_price__gt}&total_price__lt={total_price__lt}'
    url = reverse("orders-list") + '?' + params
    resp = admin_client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    for item in resp_json:
        assert item['total'] == str(order_info.total)


def test_order_filter_by_create_date_and_update_date(admin_client, client, django_user_model):
    """ Тест фильтра по дате создания и обновления """
    """ Создание списка товаров """
    url = reverse("products-list")
    product = {"name": "гвозди", "price": 10, "description": "китайские"}
    product1 = {"name": "молоток", "price": 100, "description": "для забивания китайских гвоздей"}
    product2 = {"name": "доска", "price": 15, "description": "для китайских гвоздей"}
    response = admin_client.post(url, product)
    response1 = admin_client.post(url, product1)
    response2 = admin_client.post(url, product2)
    assert response.status_code == HTTP_201_CREATED
    assert response1.status_code == HTTP_201_CREATED
    assert response2.status_code == HTTP_201_CREATED
    """ Регистрация пользователя и создание заказа """
    username = "foo"
    password = "bar"
    user = django_user_model.objects.create_user(username=username, password=password)
    client.force_login(user)
    url = reverse("orders-list")
    name = User.objects.get(pk=user.pk)
    order = {"user": name.id, "status": "NEW"}
    resp = client.post(url, order)
    assert resp.status_code == HTTP_201_CREATED
    """ Создание позиций заказа пользователем """
    order_info = Order.objects.get(user=order['user'])
    url = reverse("positions-list")
    product_info = Product.objects.get(name=product['name'])
    product_info1 = Product.objects.get(name=product1['name'])
    product_info2 = Product.objects.get(name=product2['name'])
    position = {'user': name.id, 'product': product_info.id, 'order': order_info.id, 'quantity': 100}
    position1 = {'user': name.id, 'product': product_info1.id, 'order': order_info.id, 'quantity': 1}
    position2 = {'user': name.id, 'product': product_info2.id, 'order': order_info.id, 'quantity': 5}
    response = client.post(url, position)
    response1 = client.post(url, position1)
    response2 = client.post(url, position2)
    assert response.status_code == HTTP_201_CREATED
    assert response1.status_code == HTTP_201_CREATED
    assert response2.status_code == HTTP_201_CREATED
    """ Фильтр по дате создания """
    order_info = Order.objects.get(user=order['user'])
    created_at_after = '2021-01-18'
    created_at_before = '2021-02-09'
    params = f'created_at_after={created_at_after}&created_at_before={created_at_before}'
    url = reverse("orders-list") + '?' + params
    resp = admin_client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    for item in resp_json:
        data_from_response = item['created_at'].replace('T', ' ').split('.')[0]
        data_from_db = str(order_info.created_at).split('.')[0]
        assert data_from_response == data_from_db
    """ Фильтр по дате обновления """
    order_info = Order.objects.get(user=order['user'])
    now = dt.date.today()
    delta = dt.timedelta(hours=48)
    two_days_ago = now - delta
    two_days_further = now + delta
    params = f'updated_at_after={two_days_ago}&updated_at_before={two_days_further}'
    url = reverse("orders-list") + '?' + params
    resp = admin_client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    for item in resp_json:
        data_from_response = item['updated_at'].replace('T', ' ').split('.')[0]
        data_from_db = str(order_info.updated_at).split('.')[0]
        assert data_from_response == data_from_db


def test_order_filter_by_product_in_positions(admin_client, client, django_user_model):
    """ Тест фильтра по продуктам в позициях заказа """
    """ Создание списка товаров """
    url = reverse("products-list")
    product = {"name": "гвозди", "price": 10, "description": "китайские"}
    product1 = {"name": "молоток", "price": 100, "description": "для забивания китайских гвоздей"}
    product2 = {"name": "доска", "price": 15, "description": "для китайских гвоздей"}
    response = admin_client.post(url, product)
    response1 = admin_client.post(url, product1)
    response2 = admin_client.post(url, product2)
    assert response.status_code == HTTP_201_CREATED
    assert response1.status_code == HTTP_201_CREATED
    assert response2.status_code == HTTP_201_CREATED
    """ Регистрация пользователя и создание заказа """
    username = "foo"
    password = "bar"
    user = django_user_model.objects.create_user(username=username, password=password)
    username = "vasia"
    password = "123"
    user1 = django_user_model.objects.create_user(username=username, password=password)
    username = "petya"
    password = "456"
    user2 = django_user_model.objects.create_user(username=username, password=password)
    client.force_login(user)
    client.force_login(user1)
    client.force_login(user2)
    url = reverse("orders-list")
    name = User.objects.get(pk=user.pk)
    name1 = User.objects.get(pk=user1.pk)
    name2 = User.objects.get(pk=user2.pk)
    order = {"user": name.id, "status": "NEW"}
    order1 = {"user": name1.id, "status": "NEW"}
    order2 = {"user": name2.id, "status": "NEW"}
    resp = client.post(url, order)
    resp1 = client.post(url, order1)
    resp2 = client.post(url, order2)
    assert resp.status_code == HTTP_201_CREATED
    assert resp1.status_code == HTTP_201_CREATED
    assert resp2.status_code == HTTP_201_CREATED
    """ Создание позиций заказа пользователем """
    order_info = Order.objects.get(user=order['user'])
    order_info1 = Order.objects.get(user=order1['user'])
    order_info2 = Order.objects.get(user=order2['user'])
    url = reverse("positions-list")
    product_info = Product.objects.get(name=product['name'])
    product_info1 = Product.objects.get(name=product1['name'])
    product_info2 = Product.objects.get(name=product2['name'])
    position = {'user': name.id, 'product': product_info.id, 'order': order_info.id, 'quantity': 100}
    position1 = {'user': name1.id, 'product': product_info1.id, 'order': order_info1.id, 'quantity': 1}
    position2 = {'user': name2.id, 'product': product_info2.id, 'order': order_info2.id, 'quantity': 5}
    response = client.post(url, position)
    response1 = client.post(url, position1)
    response2 = client.post(url, position2)
    assert response.status_code == HTTP_201_CREATED
    assert response1.status_code == HTTP_201_CREATED
    assert response2.status_code == HTTP_201_CREATED
    """ Фильтр по продуктам в заказах """
    name = "молоток"
    product_id = Product.objects.get(name=name).id
    position_id_from_db = Position.objects.get(product=product_id).id
    order_id_from_db = Position.objects.get(product=product_id).order.id
    params = f'position={position_id_from_db}'
    url = reverse('orders-list') + '?' + params
    resp = admin_client.get(url)
    resp_json = resp.json()
    for item in resp_json:
        order_id_from_request = item['id']
        assert order_id_from_request == order_id_from_db
