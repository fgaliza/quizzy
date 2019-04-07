from rest_framework import viewsets

from .models import Question
from .serializers import QuestionSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('-text')
    serializer_class = QuestionSerializer
