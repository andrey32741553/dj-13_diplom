from django.urls import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_204_NO_CONTENT, \
    HTTP_403_FORBIDDEN

from shop_api.models import Product, Review


def test_create_review_by_authenticated_client(client, admin_client, django_user_model):
    """ Тест создания отзыва авторизованным пользователем и проверка невозможности создания более одного отзыва"""
    url = reverse("products-list")
    product = {"name": "яблоки", "price": 50, "description": "вкусные, спелые"}
    response = admin_client.post(url, product)
    assert response.status_code == HTTP_201_CREATED
    username = "foo"
    password = "bar"
    user = django_user_model.objects.create_user(username=username, password=password)
    client.force_login(user)
    url = reverse("product-reviews-list")
    product_info = Product.objects.get(name=product['name'])
    review = {'review_text': 'хорошая вещь', 'rating': 4, 'product': product_info.id}
    response = client.post(url, review)
    assert response.status_code == HTTP_201_CREATED
    review1 = {'review_text': 'всё понравилось', 'rating': 5, 'product': product_info.id}
    resp = client.post(url, review1)
    assert resp.status_code == HTTP_400_BAD_REQUEST


def test_create_review_by_not_authenticated_client(client, admin_client):
    """ Тест невозможности создания отзыва неавторизованным пользователем """
    url = reverse("products-list")
    product = {"name": "яблоки", "price": 50, "description": "вкусные, спелые"}
    response = admin_client.post(url, product)
    assert response.status_code == HTTP_201_CREATED
    url = reverse("product-reviews-list")
    product_info = Product.objects.get(name=product['name'])
    review = {'review_text': 'хорошая вещь', 'rating': 4, 'product': product_info.id}
    response = client.post(url, review)
    assert response.status_code == HTTP_403_FORBIDDEN


def test_update_review_by_authenticated_client(client, admin_client, django_user_model):
    """ Тест обновления отзыва авторизованным пользователем"""
    """ Создание товара """
    url = reverse("products-list")
    product = {"name": "яблоки", "price": 50, "description": "вкусные, спелые"}
    response = admin_client.post(url, product)
    assert response.status_code == HTTP_201_CREATED
    """ Регистрация пользователя и создание отзыва """
    username = "foo"
    password = "bar"
    user = django_user_model.objects.create_user(username=username, password=password)
    client.force_login(user)
    url = reverse("product-reviews-list")
    product_info = Product.objects.get(name=product['name'])
    review = {'review_text': 'вкусные', 'rating': 4, 'product': product_info.id}
    response = client.post(url, review)
    assert response.status_code == HTTP_201_CREATED
    """ Обновление отзыва """
    new_review = {"review_text": "всё-таки неочень", "rating": 2, "product": product_info.id}
    review_info = Review.objects.get(review_text=review["review_text"])
    url = reverse("product-reviews-detail", args=(review_info.id,))
    resp = client.put(url, data=new_review, content_type='application/json')
    new_review_info = Review.objects.get(review_text=new_review['review_text'])
    assert resp.status_code == HTTP_200_OK
    assert new_review_info.rating == 2


def test_destroy_review_by_authenticated_client(client, admin_client, django_user_model):
    """ Тест удаления отзыва авторизованным пользователем """
    """ Создание товара """
    url = reverse("products-list")
    product = {"name": "яблоки", "price": 50, "description": "вкусные, спелые"}
    response = admin_client.post(url, product)
    assert response.status_code == HTTP_201_CREATED
    """ Регистрация пользователя и создание отзыва """
    username = "foo"
    password = "bar"
    user = django_user_model.objects.create_user(username=username, password=password)
    client.force_login(user)
    url = reverse("product-reviews-list")
    product_info = Product.objects.get(name=product['name'])
    review = {'review_text': 'вкусные', 'rating': 4, 'product': product_info.id}
    response = client.post(url, review)
    assert response.status_code == HTTP_201_CREATED
    """ Удаление отзыва """
    review_info = Review.objects.get(review_text=review["review_text"])
    url = reverse("product-reviews-detail", args=(review_info.id,))
    resp = client.delete(url)
    assert resp.status_code == HTTP_204_NO_CONTENT


def test_filter_review_by_product(client, admin_client, django_user_model):
    """ Тест фильтра отзывов по продуктам """
    url = reverse("products-list")
    product = {"name": "яблоки", "price": 50, "description": "вкусные, спелые"}
    product1 = {"name": "груши", "price": 70, "description": "вкусные, сочные, спелые"}
    product2 = {"name": "бананы", "price": 80, "description": "сладкие"}
    response = admin_client.post(url, product)
    response1 = admin_client.post(url, product1)
    response2 = admin_client.post(url, product2)
    assert response.status_code == HTTP_201_CREATED
    assert response1.status_code == HTTP_201_CREATED
    assert response2.status_code == HTTP_201_CREATED
    """ Регистрация пользователя и создание отзывов """
    username = "foo"
    password = "bar"
    user = django_user_model.objects.create_user(username=username, password=password)
    client.force_login(user)
    url = reverse("product-reviews-list")
    product_info = Product.objects.get(name=product['name'])
    product_info1 = Product.objects.get(name=product1['name'])
    product_info2 = Product.objects.get(name=product2['name'])
    review = {'review_text': 'нормальные', 'rating': 4, 'product': product_info.id}
    review1 = {'review_text': 'съедобные', 'rating': 3, 'product': product_info1.id}
    review2 = {'review_text': 'сладкие', 'rating': 5, 'product': product_info2.id}
    response = client.post(url, review)
    response1 = client.post(url, review1)
    response2 = client.post(url, review2)
    assert response.status_code == HTTP_201_CREATED
    assert response1.status_code == HTTP_201_CREATED
    assert response2.status_code == HTTP_201_CREATED
    """ Фильтр отзывов по продуктам """
    params = f'product={product_info2.id}'
    url = reverse("product-reviews-list") + '?' + params
    resp = client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    for item in resp_json:
        assert item['product'] == str(product_info2.name)
