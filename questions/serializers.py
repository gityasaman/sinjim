from rest_framework import serializers
from .models import Question, Answer
from taggit_serializer.serializers import TaggitSerializer, TagListSerializerField

class QuestionSerializer(serializers.ModelSerializer, TaggitSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Question
        fields = ['title', 'body', 'tags']

class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['body']

