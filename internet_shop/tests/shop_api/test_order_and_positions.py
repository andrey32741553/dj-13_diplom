import pytest
from django.contrib.auth.models import User

from django.urls import reverse
from rest_framework.status import HTTP_200_OK

from shop_api.models import Order, Product, Position
import datetime as dt


@pytest.mark.django_db
def test_get_list_of_orders_by_admin(product_factory, admin_client, create_order_by_authenticated_user):
    """ Тест на вывод списка заказов """
    product_factory(_quantity=3)
    create_order_by_authenticated_user()
    url = reverse("orders-list")
    resp = admin_client.get(url)
    assert resp.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_get_own_list_of_orders_by_authenticated_user(authenticated_client,
                                                      create_order_by_authenticated_user):
    """ Тест на получение своего заказа пользователем"""
    create_order_by_authenticated_user()
    user = User.objects.get(username='foo').id
    order_info = Order.objects.get(user=user)
    url = reverse("orders-detail", args=(order_info.id,))
    resp = authenticated_client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert str(order_info.user) == resp_json['user']


@pytest.mark.django_db
def test_order_filter_by_total_price(create_order_by_authenticated_user,
                                     authenticated_client, admin_client):
    """ Тест фильтра по итоговой цене """
    create_order_by_authenticated_user()
    user = User.objects.get(username='foo').id
    order_info = Order.objects.get(user=user)
    total_price__gt = 10
    total_price__lt = 1200
    params = f'total_price__gt={total_price__gt}&total_price__lt={total_price__lt}'
    url = reverse("orders-list") + '?' + params
    resp = admin_client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    for item in resp_json:
        assert item['total'] == order_info.total


@pytest.mark.django_db
def test_order_filter_by_create_date(create_order_by_authenticated_user,
                                     authenticated_client, admin_client):
    """ Тест фильтра по дате создания """
    create_order_by_authenticated_user()
    user = User.objects.get(username='foo').id
    order_info = Order.objects.get(user=user)
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


@pytest.mark.django_db
def test_order_filter_by_update_date(create_order_by_authenticated_user,
                                     authenticated_client, admin_client):
    """ Тест фильтра по дате создания """
    create_order_by_authenticated_user()
    user = User.objects.get(username='foo').id
    order_info = Order.objects.get(user=user)
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


@pytest.mark.django_db
def test_order_filter_by_product_in_positions(create_order_by_authenticated_user,
                                              authenticated_client, admin_client):
    """ Тест фильтра по продуктам в позициях заказа """
    order = create_order_by_authenticated_user()
    product_id = Product.objects.get(id=order['products'][0]['product'])
    position_id_from_db = Position.objects.get(product=product_id).id
    order_id_from_db = Position.objects.get(product=product_id).order.id
    params = f'position={position_id_from_db}'
    url = reverse('orders-list') + '?' + params
    resp = admin_client.get(url)
    resp_json = resp.json()
    for item in resp_json:
        order_id_from_request = item['id']
        assert order_id_from_request == order_id_from_db
