from django.db import models


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
