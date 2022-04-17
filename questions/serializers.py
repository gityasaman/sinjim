from rest_framework import serializers
from .models import Question, Answer
from .models import QuestionTag
from taggit_serializer.serializers import TaggitSerializer, TagListSerializerField

class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['body']

class QuestionSerializer(serializers.ModelSerializer, TaggitSerializer):
    tags = TagListSerializerField()
    answers = serializers.StringRelatedField(many=True)
    upvoters = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['title', 'body', 'tags', 'answers', 'created', 'upvoters']

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        instance = super(QuestionSerializer, self).create(validated_data)
        instance.tags.set(tags)
        return instance

class VerifyAnswerSerializer(serializers.Serializer):
    verified_answer = serializers.CharField()

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionTag
        fields = ['name']