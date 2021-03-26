import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK

from shop_api.models import ProductCollections


@pytest.mark.django_db
def test_add_products_to_product_collections_by_admin(admin_client, client,
                                                      create_product_collections_by_admin):
    """ Тест добавления товаров в подборки админом """
    create_product_collections_by_admin()
    """ Изменение информации о подборке админом """
    new_text = {'title': 'для дома и развлечений', 'text': 'отличная техника для дома и развлечений'}
    collection_info = ProductCollections.objects.get(title='для развлечений')
    url = reverse("product-collections-detail", args=(collection_info.id,))
    resp = admin_client.put(url, data=new_text, format='json')
    new_collection = ProductCollections.objects.get(title=new_text['title'])
    assert resp.status_code == HTTP_200_OK
    assert new_collection.text == "отличная техника для дома и развлечений"
    """ Получение списка подборок пользователем """
    url = reverse("product-collections-list")
    resp = client.get(url)
    assert resp.status_code == HTTP_200_OK
