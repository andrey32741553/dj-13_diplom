import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_favourites(add_product_to_favourites_list):
    """ Добавление пользователем товара в избранное """
    response = add_product_to_favourites_list
    assert response.status_code == HTTP_201_CREATED


@pytest.mark.django_db
def test_get_list_of_favourites_by_authenticated_user(authenticated_client, add_product_to_favourites_list):
    """ Получение списка избранных товаров пользователем """
    add_product_to_favourites_list
    url = reverse("user-info-list")
    resp = authenticated_client.get(url)
    assert resp.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_get_own_list_of_favouritess_by_authenticated_user(authenticated_client, add_product_to_favourites_list, django_user_model):
    """ Получение своего списка избранных товаров пользователем """
    add_product_to_favourites_list
    favourites_info = User.objects.get(username="foo")
    url = reverse("user-info-detail", args=(favourites_info.id,))
    resp = authenticated_client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert str(favourites_info.username) == resp_json['username']
    """ Тест на отказ при попытке получить чужой список. Создаём ещё одного пользователя """
    username1 = "vasia"
    password1 = "123456"
    user1 = django_user_model.objects.create_user(username=username1, password=password1)
    authenticated_client.force_login(user1)
    another_user = User.objects.get(username=username1)
    url = reverse("user-info-detail", args=(favourites_info.id,))
    resp = authenticated_client.get(url)
    assert resp.status_code == HTTP_400_BAD_REQUEST
    assert str(another_user) != favourites_info.username
