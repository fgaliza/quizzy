import factory

from apps.quizzes.models import Choice, Question, Quiz
from tests.users.factories import AppUserFactory


class QuestionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Question

    text = 'Are you afraid of spiders?'


class ChoiceFactory(factory.DjangoModelFactory):
    class Meta:
        model = Choice

    question = factory.SubFactory(QuestionFactory)
    text = 'Yes'


class QuizFactory(factory.DjangoModelFactory):
    class Meta:
        model = Quiz

    user = factory.SubFactory(AppUserFactory)

    @factory.post_generation
    def questions(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for question in extracted:
                self.questions.add(question)
