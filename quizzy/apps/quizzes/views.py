from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Choice, Question
from .serializers import ChoiceSerializer, QuestionSerializer


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
