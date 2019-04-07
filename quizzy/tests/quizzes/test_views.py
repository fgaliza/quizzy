import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from .factories import ChoiceFactory, QuestionFactory

pytestmark = pytest.mark.django_db

# Question


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


# Choice


def test_get_choices_return_none(client):
    question = QuestionFactory()
    url = reverse('quizzes:choices-list', [question.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['results'] == []
    assert response.data['count'] == 0


def test_get_all_choices_for_question(client):
    question = QuestionFactory()
    choice = ChoiceFactory(question=question)
    url = reverse('quizzes:choices-list', [question.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['results'][0]['text'] == choice.text


def test_get_choice(client):
    question = QuestionFactory()
    choice = ChoiceFactory(question=question)
    url = reverse('quizzes:choices-detail', [question.id, choice.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['text'] == choice.text


def test_create_choice(client, choice_payload):
    question = QuestionFactory()
    url = reverse('quizzes:choices-list', [question.id])
    response = client.post(url, choice_payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['text'] == choice_payload['text']


def test_create_duplicate_choice(client, choice_payload):
    question = QuestionFactory()
    ChoiceFactory(text='Yes', question=question)
    url = reverse('quizzes:choices-list', [question.id])
    response = client.post(url, choice_payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_choice_without_required_fields(client, choice_payload):
    question = QuestionFactory()
    del choice_payload['text']
    url = reverse('quizzes:choices-list', [question.id])
    response = client.post(url, choice_payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_choice_for_invalid_question(client, choice_payload):
    url = reverse('quizzes:choices-list', [1])
    response = client.post(url, choice_payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_patch_choice(client, choice_payload):
    question = QuestionFactory()
    choice = ChoiceFactory(question=question)
    choice_payload['text'] = 'No'
    url = reverse('quizzes:choices-detail', [question.id, choice.id])
    response = client.patch(url, choice_payload)
    assert response.status_code == status.HTTP_200_OK


def test_delete_choice(client):
    question = QuestionFactory()
    choice = ChoiceFactory(question=question)
    url = reverse('quizzes:choices-detail', [question.id, choice.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
