import pytest


@pytest.fixture
def question_payload():
    return {
        'text': 'Is the cake a lie?',
    }


@pytest.fixture
def choice_payload():
    return {
        'text': 'Yes',
    }
