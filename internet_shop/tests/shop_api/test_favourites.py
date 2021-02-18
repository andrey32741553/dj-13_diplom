from django.urls import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_400_BAD_REQUEST

from shop_api.models import Product, UserMethods


def test_create_favourites_by_authenticated_client(client, admin_client, django_user_model):
    """ Тест добавления товаров в избранные авторизованным пользователем """
    """ Создание списка товаров админом """
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
    """ Регистрация пользователей """
    username = "foo"
    password = "bar"
    user = django_user_model.objects.create_user(username=username, password=password)
    client.force_login(user)
    """ Добавление пользователем товара в избранное """
    url = reverse("favourites-list")
    product_info = Product.objects.get(name=product['name'])
    favourite_product = {'product': product_info.id}
    response = client.post(url, favourite_product)
    assert response.status_code == HTTP_201_CREATED
    """ Получение списка избранных товаров пользователем """
    url = reverse("user-info-list")
    resp = client.get(url)
    assert resp.status_code == HTTP_200_OK
    """ Получение своего списка избранных товаров пользователем """
    favourites_info = UserMethods.objects.get(username=username)
    url = reverse("user-info-detail", args=(favourites_info.id,))
    resp = client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert str(favourites_info.username) == resp_json['username']
    """ Тест на отказ при попытке получить чужой список. Создаём ещё одного пользователя """
    username1 = "vasia"
    password1 = "123456"
    user1 = django_user_model.objects.create_user(username=username1, password=password1)
    client.force_login(user1)
    another_user = UserMethods.objects.get(username=username1)
    url = reverse("user-info-detail", args=(favourites_info.id,))
    resp = client.get(url)
    assert resp.status_code == HTTP_400_BAD_REQUEST
    assert str(another_user) != favourites_info.username
