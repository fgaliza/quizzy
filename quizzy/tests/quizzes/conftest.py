import pytest


@pytest.fixture
def question_payload():
    return {
        'text': 'Is the cake a lie?',
    }
