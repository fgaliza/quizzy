import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from .factories import AppUserFactory

pytestmark = pytest.mark.django_db


def test_get_user_return_none(client):
    url = reverse('users:users-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['results'] == []
    assert response.data['count'] == 0


def test_get_all_users(client):
    user = AppUserFactory()
    url = reverse('users:users-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['results'][0]['name'] == user.name


def test_get_app_user_detail_by_id(client):
    user = AppUserFactory()
    url = reverse('users:users-detail', [user.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == user.name


def test_create_app_user(client, app_user_payload):
    url = reverse('users:users-list')
    response = client.post(url, app_user_payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == app_user_payload['name']


def test_create_without_required_fields(client, app_user_payload):
    del app_user_payload['name']
    url = reverse('users:users-list')
    response = client.post(url, app_user_payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_patch_app_user(client, app_user_payload):
    user = AppUserFactory()
    app_user_payload['name'] = 'John Doe'
    url = reverse('users:users-detail', [user.id])
    response = client.patch(url, app_user_payload)
    assert response.status_code == status.HTTP_200_OK


def test_delete_app_user(client):
    user = AppUserFactory()
    url = reverse('users:users-detail', [user.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
