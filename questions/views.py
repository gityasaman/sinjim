from django.shortcuts import render, get_object_or_404
from rest_framework import generics, mixins
from rest_framework.views import APIView, View
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer, VerifyAnswerSerializer
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
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        serializer = QuestionSerializer(question)
        return Response({'question': serializer.data}) 
    
    def post(self, request, pk):
        question_id = Question.objects.get(pk=pk)
        if request.user != question_id.questioner:
            serializer = AnswerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(answerer_id=request.user.id, question_id=question_id)   
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            print(question_id.questioner)
            serializer = VerifyAnswerSerializer(data=request.data)
            if serializer.is_valid():
                answer_id = serializer.validated_data['verified_answer']
                answer = get_object_or_404(Answer, pk=answer_id)
                question_id.verified_answer = answer
                return Response(serializer.data)
            else:
                return Response(serializer.errors)

# class QuestionUpdateView(generics.UpdateAPIView):
#     serializer_class = QuestionSerializer
#     queryset = Question.objects.all()

class UpvoteQuestionView(APIView):
    user = get_user_model()

    def get(self, request, pk):
        question = Question.objects.get(pk=pk)
        upvoters = question.upvoters.all()
        if request.user in upvoters:
            question.upvoters.remove(request.user)
            return Response({'message': 'undo upvote'})
        else:
            question.upvoters.add(request.user)
            return Response({'message': 'upvoted'})
