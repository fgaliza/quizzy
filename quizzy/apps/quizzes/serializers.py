from rest_framework import serializers

from .models import Choice, Question


class ChoiceSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=200)

    def create(self, validated_data):
        return Choice.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('text', 'choices')
