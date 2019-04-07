import pytest
from django.db import IntegrityError

from apps.quizzes.models import Question

pytestmark = pytest.mark.django_db


def test_question():
    text = 'Are you afraid of spiders?'
    question = Question.objects.create(text=text)
    assert question
    assert question.text == text


def test_question_without_required_fields():
    with pytest.raises(IntegrityError):
        Question.objects.create(text=None)
