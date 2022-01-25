from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer
from rest_framework.response import Response
from django.contrib.auth import get_user_model

class QuestionViewSet(viewsets.ModelViewSet):

    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        user = get_user_model()
        if serializer.is_valid(): 
            serializer.save(questioner=request.user)
            return Response({'data': request.data})
        else:
            return Response(serializer.errors)
    
    def retrieve(self, request, pk=None):
        question = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(question)
        return Response(serializer.data)

class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
