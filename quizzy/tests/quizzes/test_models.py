import pytest
from django.db import IntegrityError

from apps.quizzes.models import Choice, Question

from .factories import QuestionFactory

pytestmark = pytest.mark.django_db


def test_question():
    text = 'Are you afraid of spiders?'
    question = Question.objects.create(text=text)
    assert question
    assert question.text == text


def test_question_without_required_fields():
    with pytest.raises(IntegrityError):
        Question.objects.create(text=None)


def test_choice_without_required_fields():
    with pytest.raises(IntegrityError):
        text = 'Yes'
        Choice.objects.create(text=text)


def test_choice():
    text = 'Yes'
    question = QuestionFactory()
    choice = Choice.objects.create(text=text, question=question)
    assert choice
    assert choice.text == text
