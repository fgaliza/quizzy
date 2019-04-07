import pytest

from apps.users.serializers import AppUserSerializer

pytestmark = pytest.mark.django_db


def test_appuser_serializer(app_user_payload):
    serializer = AppUserSerializer(data=app_user_payload)
    assert serializer.is_valid() is True
    assert serializer.data['name'] == app_user_payload['name']


def test_appuser_serializer_without_required_fields(app_user_payload):
    del app_user_payload['name']
    serializer = AppUserSerializer(data=app_user_payload)
    assert serializer.is_valid() is False
