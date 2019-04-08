import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0003_add_quiz_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='quizzes.Choice')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='quizzes.Question')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='quizzes.Quiz')),
            ],
            options={
                'unique_together': {('quiz', 'question', 'choice')},
            },
        ),
    ]
