from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer
from rest_framework.response import Response
from django.contrib.auth import get_user_model

class CreateQuestionView(generics.CreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        user = get_user_model()
        if serializer.is_valid():
            serializer.save(questioner = request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class QuestionListView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

class QuestionDetailView(APIView):
    user = get_user_model()
    serializer_class = AnswerSerializer

    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        serializer = QuestionSerializer(question)
        return Response({'question': serializer.data})
    
    def post(self, request, pk):
        question_id = Question.objects.get(pk=pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(): 
            serializer.save(answerer_id=request.user.id, question_id=question_id)   
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class CreateAnswerView(generics.CreateAPIView):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]