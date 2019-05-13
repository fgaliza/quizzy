import binascii
import json

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from .models import Choice, Question, Quiz
from .serializers import AnswerSerializer, ChoiceSerializer, QuestionSerializer, QuizSerializer
from apps.users.models import AppUser
from apps.users.serializers import AppUserSerializer
from apps.utils import url_decrypt


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('-text')
    serializer_class = QuestionSerializer


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all().order_by('-question')
    serializer_class = ChoiceSerializer


class QuizViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Quiz.objects.all().order_by('-text')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AnswerSerializer
        return QuizSerializer

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

    def create(self, request, *args, **kwargs):
        data = json.loads(request.data)
        username = data.get('user')

        if not username:
            return Response(
                'No user sent',
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = AppUser.objects.get(name=username)
        except ObjectDoesNotExist:
            user_serializer = AppUserSerializer(data={'name': username})
            if user_serializer.is_valid():
                user = user_serializer.save()
            else:
                return Response(
                    'Invalid username',
                    status=status.HTTP_400_BAD_REQUEST,
                )

        answers = data.get('answers')

        if not answers:
            return Response(
                'No answers sent',
                status=status.HTTP_400_BAD_REQUEST,
            )

        for answer in answers:
            question = Question.objects.get(id=answer['question'])
            choice = Choice.objects.get(text=answer['choice'])
            answer_data = {
                'question': question.__dict__,
                'choice': choice.__dict__,
            }
            serializer = AnswerSerializer(data=answer_data)

            if not serializer.is_valid():
                return Response(
                    'Invalid answer payload',
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save(user=user)

# This would return a link for this quiz answered by the user
# Detail route would be a user answering an existing quiz answered by other user.
# The Response for the detail route would be the statistics of the questions
