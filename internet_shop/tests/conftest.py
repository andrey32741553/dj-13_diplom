import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from django.conf import settings


@pytest.fixture
def product_factory():
    def factory(**kwargs):
        course = baker.make('shop_api.Product', **kwargs)
        return course
    return factory


@pytest.fixture
def review_factory():
    def factory(**kwargs):
        course = baker.make('shop_api.Review', **kwargs)
        return course
    return factory


@pytest.fixture
def order_factory():
    def factory(**kwargs):
        course = baker.make('shop_api.Order', **kwargs)
        return course
    return factory


@pytest.fixture
def collection_factory():
    def factory(**kwargs):
        course = baker.make('shop_api.ProductCollections', **kwargs)
        return course
    return factory

@pytest.fixture
def position_factory():
    def factory(**kwargs):
        course = baker.make('shop_api.Position', **kwargs)
        return course
    return factory

@pytest.fixture
def productlistforcollection_factory():
    def factory(**kwargs):
        course = baker.make('shop_api.ProductListForCollection', **kwargs)
        return course
    return factory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def settings():
    return settings
