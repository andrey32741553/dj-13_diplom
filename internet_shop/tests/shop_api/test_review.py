import pytest
from django.urls import reverse
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_204_NO_CONTENT, \
    HTTP_403_FORBIDDEN

from shop_api.models import Product, Review


@pytest.mark.django_db
def test_create_review_by_authenticated_client(authenticated_client, product_factory, create_review_by_authenticated_user):
    """ Тест создания отзыва авторизованным пользователем и проверка невозможности создания более одного отзыва"""
    url = reverse("product-reviews-list")
    product_factory(_quantity=3)
    product_info, review = create_review_by_authenticated_user
    review1 = {'review_text': 'всё понравилось', 'rating': 5, 'product': product_info.id}
    resp = authenticated_client.post(url, review1)
    assert resp.status_code == HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_review_by_not_authenticated_client(client, product_factory):
    """ Тест невозможности создания отзыва неавторизованным пользователем """
    product = product_factory(_quantity=3)
    url = reverse("product-reviews-list")
    product_info = Product.objects.get(name=product[0])
    review = {'review_text': 'хорошая вещь', 'rating': 4, 'product': product_info.id}
    response = client.post(url, review)
    assert response.status_code == HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_update_review_by_authenticated_client(product_factory, authenticated_client, create_review_by_authenticated_user):
    """ Тест обновления отзыва авторизованным пользователем"""
    product_factory(_quantity=3)
    product_info, review = create_review_by_authenticated_user
    new_review = {"review_text": "всё-таки неочень", "rating": 2, "product": product_info.id}
    review_info = Review.objects.get(review_text=review["review_text"])
    url = reverse("product-reviews-detail", args=(review_info.id,))
    resp = authenticated_client.put(url, data=new_review, content_type='application/json')
    new_review_info = Review.objects.get(review_text=new_review['review_text'])
    assert resp.status_code == HTTP_200_OK
    assert new_review_info.rating == 2


@pytest.mark.django_db
def test_destroy_review_by_authenticated_client(product_factory, create_review_by_authenticated_user, authenticated_client):
    """ Тест удаления отзыва авторизованным пользователем """
    product_factory(_quantity=3)
    product_info, review = create_review_by_authenticated_user
    review_info = Review.objects.get(review_text=review["review_text"])
    url = reverse("product-reviews-detail", args=(review_info.id,))
    resp = authenticated_client.delete(url)
    assert resp.status_code == HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_filter_review_by_product(product_factory, authenticated_client, create_review_by_authenticated_user):
    """ Тест фильтра отзывов по продуктам """
    product_factory(_quantity=3)
    product_info, review = create_review_by_authenticated_user
    params = f'product={product_info.id}'
    url = reverse("product-reviews-list") + '?' + params
    resp = authenticated_client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    for item in resp_json:
        assert item['product'] == product_info.id
