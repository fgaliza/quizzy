import factory

from apps.quizzes.models import Question, Choice


class QuestionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Question

    text = 'Are you afraid of spiders?'


class ChoiceFactory(factory.DjangoModelFactory):
    class Meta:
        model = Choice

    question = factory.SubFactory(QuestionFactory)
    text = 'Yes'
