from apps.utils import url_encrypt, url_decrypt
import pytest
import json


@pytest.fixture
def encrypted_string():
    return 'eyJxdWl6X2lkIjogMX0='


def test_url_encrypt(encrypted_string):
    url_data = url_encrypt(
        quiz_id=1,
    )
    assert url_data == encrypted_string


def test_url_decrypt(encrypted_string):
    decripted_data = json.loads(url_decrypt(encrypted_string))
    assert decripted_data['quiz_id'] == 1