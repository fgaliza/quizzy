import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from .factories import QuestionFactory

pytestmark = pytest.mark.django_db


def test_get_questions_return_none(client):
    url = reverse('quizzes:questions-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['results'] == []
    assert response.data['count'] == 0


def test_get_all_questions(client):
    question = QuestionFactory()
    url = reverse('quizzes:questions-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['results'][0]['text'] == question.text


def test_get_question(client):
    question = QuestionFactory()
    url = reverse('quizzes:questions-detail', [question.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['text'] == question.text


def test_create_question(client, question_payload):
    url = reverse('quizzes:questions-list')
    response = client.post(url, question_payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['text'] == question_payload['text']


def test_create_duplicate_question(client, question_payload):
    QuestionFactory(text=question_payload['text'])
    url = reverse('quizzes:questions-list')
    response = client.post(url, question_payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_without_required_fields(client, question_payload):
    del question_payload['text']
    url = reverse('quizzes:questions-list')
    response = client.post(url, question_payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_patch_question(client, question_payload):
    question = QuestionFactory()
    question_payload['text'] = 'Have you ever been to Germany?'
    url = reverse('quizzes:questions-detail', [question.id])
    response = client.patch(url, question_payload)
    assert response.status_code == status.HTTP_200_OK


def test_delete_question(client):
    question = QuestionFactory()
    url = reverse('quizzes:questions-detail', [question.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
