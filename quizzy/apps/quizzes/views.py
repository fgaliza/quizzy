import binascii
import json

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from .models import Choice, Question, Quiz
from .serializers import ChoiceSerializer, QuestionSerializer, QuizSerializer
from apps.utils import url_decrypt


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('-text')
    serializer_class = QuestionSerializer


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all().order_by('-question')
    serializer_class = ChoiceSerializer

    def create(self, request, *args, **kwargs):
        question_id = kwargs['nested_1_pk']
        text = request.data.get('text')

        try:
            question = Question.objects.get(id=question_id)
        except ObjectDoesNotExist:
            return Response(
                'Question does not exist',
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not text:
            return Response(
                'Invalid choice text',
                status=status.HTTP_400_BAD_REQUEST,
            )

        if question.choices.filter(text=text):
            return Response(
                'Choice text already registered for this question',
                status=status.HTTP_400_BAD_REQUEST,
            )

        choice = {
            'question': question_id,
            'text': text
        }

        serializer = ChoiceSerializer(data=choice)

        if not serializer.is_valid():
            return Response(
                'Invalid choice payload',
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save(question_id=question_id)

        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class QuizViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Quiz.objects.all().order_by('-text')
    serializer_class = QuizSerializer

    def list(self, request, *args, **kwargs):
        random_questions = Question.objects.all().order_by('?')[:settings.QUESTIONS_PER_QUIZ]
        data = {
            'questions': random_questions,
        }
        serializer = QuizSerializer(data)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        try:
            data = json.loads(url_decrypt(kwargs['pk']))
        except (binascii.Error, ValueError):
            return Response(
                'Quiz does not exist',
                status=status.HTTP_400_BAD_REQUEST,
            )

        quiz_id = data.get('quiz_id')

        if not quiz_id:
            return Response(
                'Quiz does not exist',
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except ObjectDoesNotExist:
            return Response(
                'Quiz does not exist',
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = QuizSerializer(quiz)
        return Response(serializer.data)
