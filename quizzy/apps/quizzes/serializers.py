from rest_framework import serializers

from .models import Answer, Choice, Question, Quiz


class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = ('text', 'question',)


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('text', 'choices',)


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ('questions',)


class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(write_only=True)
    choice = ChoiceSerializer(write_only=True)

    class Meta:
        model = Answer
        fields = ('question', 'choice',)
