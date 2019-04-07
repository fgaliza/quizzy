import pytest
from django.db import IntegrityError

from apps.users.models import AppUser

pytestmark = pytest.mark.django_db


def test_user_without_required_fields():
    with pytest.raises(IntegrityError):
        AppUser.objects.create(name=None)


def test_user_duplicate_name():
    with pytest.raises(IntegrityError):
        AppUser.objects.create(name='John Doe',)
        AppUser.objects.create(name='John Doe',)
