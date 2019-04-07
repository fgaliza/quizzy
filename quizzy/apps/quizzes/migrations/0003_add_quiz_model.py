from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('quizzes', '0002_add_choice_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questions', models.ManyToManyField(related_name='quiz', to='quizzes.Question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.AppUser')),
            ],
        ),
    ]
