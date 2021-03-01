import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from model_bakery import baker
from rest_framework.status import HTTP_201_CREATED

from shop_api.models import Product, Order, UserMethods


@pytest.fixture
def authenticated_client(client, django_user_model):
    username = "foo"
    password = "bar"
    user = django_user_model.objects.create_user(username=username, password=password)
    client.force_login(user)
    return client


@pytest.fixture
def product_factory():
    def factory(**kwargs):
        product = baker.make('shop_api.Product', **kwargs)
        return product
    return factory


@pytest.fixture
def add_product_to_favourites_list(product_factory, authenticated_client):
    product = product_factory(_quantity=3)
    favourites_info = UserMethods.objects.get(username="foo")
    url = reverse("user-info-detail", args=(favourites_info.id,))
    favourites = {"products": [product[0].id, product[1].id, product[2].id]}
    response = authenticated_client.post(url, favourites)
    return response


@pytest.fixture
def create_review_by_authenticated_user(product_factory, authenticated_client):
    product = product_factory(_quantity=3)
    url = reverse("product-reviews-list")
    product_info = Product.objects.get(name=product[0])
    review = {'review_text': 'хорошая вещь', 'rating': 4, 'product': product_info.id}
    response = authenticated_client.post(url, review)
    assert response.status_code == HTTP_201_CREATED
    return product_info, review


@pytest.fixture
def create_order_by_authenticated_user(authenticated_client):
    url = reverse("orders-list")
    name = User.objects.get(username='foo')
    order = {"user": name.id, "status": "NEW"}
    resp = authenticated_client.post(url, order)
    assert resp.status_code == HTTP_201_CREATED
    return order, name


@pytest.fixture
def create_positions_by_authenticated_user(authenticated_client, create_order_by_authenticated_user, product_factory):
    product = product_factory(_quantity=3)
    order, name = create_order_by_authenticated_user
    order_info = Order.objects.get(user=order['user'])
    url = reverse("positions-list")
    product_info = Product.objects.get(name=product[0])
    product_info1 = Product.objects.get(name=product[1])
    product_info2 = Product.objects.get(name=product[2])
    position = {'user': name.id, 'product': product_info.id, 'order': order_info.id, 'quantity': 100}
    position1 = {'user': name.id, 'product': product_info1.id, 'order': order_info.id, 'quantity': 1}
    position2 = {'user': name.id, 'product': product_info2.id, 'order': order_info.id, 'quantity': 5}
    response = authenticated_client.post(url, position)
    response1 = authenticated_client.post(url, position1)
    response2 = authenticated_client.post(url, position2)
    assert response.status_code == HTTP_201_CREATED
    assert response1.status_code == HTTP_201_CREATED
    assert response2.status_code == HTTP_201_CREATED
    return position, position1, position2


@pytest.fixture
def create_product_collections_by_admin(authenticated_client, create_order_by_authenticated_user,
                                        product_factory, admin_client):
    product_factory(_quantity=4)
    product = Product.objects.all()
    url = reverse("product-collections-list")
    collection = {"title": "для работы", "text": "надёжная техника для работы", "products": [product[0].id,
                                                                                             product[3].id]}
    collection1 = {"title": "для развлечений", "text": "техника для развлечений", "products": [product[1].id,
                                                                                               product[2].id]}
    response = admin_client.post(url, collection)
    response1 = admin_client.post(url, collection1)
    assert response.status_code == HTTP_201_CREATED
    assert response1.status_code == HTTP_201_CREATED
    return collection, collection1
