import pytest


@pytest.fixture
def app_user_payload():
    return {
        'name': 'John Doe',
    }
