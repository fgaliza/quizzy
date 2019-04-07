import factory

from apps.quizzes.models import Question


class QuestionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Question

    text = 'Are you afraid of spiders?'
