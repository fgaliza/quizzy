from django.db import models

from apps.users.models import AppUser


class Question(models.Model):
    text = models.CharField(max_length=200, unique=True)


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices',
    )
    text = models.CharField(max_length=200)

    class Meta:
        unique_together = ('question', 'text')


class Quiz(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, db_index=True)
    questions = models.ManyToManyField(Question, related_name='quiz')


class Answer(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='answer', db_index=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer')
    choice = models.OneToOneField(Choice, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('quiz', 'question', 'choice')
