import pytest

from apps.quizzes.serializers import QuestionSerializer

pytestmark = pytest.mark.django_db


def test_question_serializer(question_payload):
    serializer = QuestionSerializer(data=question_payload)
    assert serializer.is_valid() is True
    assert serializer.data['text'] == question_payload['text']


def test_question_serializer_without_required_fields(question_payload):
    del question_payload['text']
    serializer = QuestionSerializer(data=question_payload)
    assert serializer.is_valid() is False
