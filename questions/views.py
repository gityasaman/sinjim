from django.shortcuts import render, get_object_or_404
from rest_framework import generics, mixins, filters
from rest_framework.views import APIView, View
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer, VerifyAnswerSerializer, TagSerializer
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from rest_framework import filters
from taggit.models import Tag
from rest_framework.decorators import action

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

    def get(self, request, tag_slug=None):
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            questions =  Question.objects.filter(tags__in=[tag])
            print(tag)
            print(tag_slug)
            serializer = QuestionSerializer(questions, many=True)
            return Response(serializer.data)
        else:
            questions =  Question.objects.all()
            serializer = QuestionSerializer(questions, many=True)
            return Response(serializer.data)
    
        
class QuestionDetailView(APIView):
    user = get_user_model()
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_object(self, pk):
        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        serializer = QuestionSerializer(question)
        return Response({'question': serializer.data}) 
    
    def post(self, request, pk):
        question_id = get_object_or_404(Question, pk)
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
    
    def delete(self, request, pk, format=None):
        question = self.get_object(pk)
        question.delete()
        return Response({'message': 'deleted successfully'})

class QuestionUpdateView(generics.UpdateAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

class UpvoteQuestionView(APIView):
    user = get_user_model()
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        question = Question.objects.get(pk=pk)
        upvoters = question.upvoters.all()
        if request.user in upvoters:
            question.upvoters.remove(request.user)
            return Response({'message': 'undo upvote'})
        else:
            question.upvoters.add(request.user)
            return Response({'message': 'upvoted'})

class UpvoteAnswerView(APIView):
    user = get_user_model()
    queryset = Answer.objects.all()
    
    def get(self, request, pk):
        answer = Answer.objects.get(pk=pk)
        upvoters = answer.upvoters.all()
        downvoters = answer.downvoters.all()
        if request.user in upvoters:
            answer.upvoters.remove(request.user)
            return Response({'message': 'Upvote removed'})
        elif request.user not in upvoters and request.user in downvoters:
            answer.downvoters.remove(request.user)
            answer.upvoters.add(request.user)
            return Response({'message': 'answer upvoted and downvote removed'})
        else:
            answer.upvoters.add(request.user)
            return Response({'message': 'answer upvoted'})

class DownvoteAnswerView(APIView):
    user = get_user_model()
    queryset = Answer.objects.all()
    
    def get(self, request, pk):
        answer = Answer.objects.get(pk=pk)
        upvoters = answer.upvoters.all()
        downvoters = answer.downvoters.all()
        if request.user in downvoters:
            answer.downvoters.remove(request.user)
            return Response({'message': 'Undo downvote'})
        elif request.user not in downvoters and request.user in upvoters:
            answer.upvoters.remove(request.user)
            answer.downvoters.add(request.user)
            return Response({'message': 'answer downvoted and upvote removed'})
        else:
            answer.downvoters.add(request.user)
            return Response({'message': 'answer downvoted'})

class AnswerDetailView(APIView):
    user = get_user_model()

    def get_object(self, pk):
        try:
            return Answer.objects.get(pk=pk)
        except Answer.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        answer = get_object_or_404(Answer, pk=pk)
        serializer = AnswerSerializer(answer)
        return Response(serializer.data)
    
    def delete(self, request, pk, format=None):
        answer = self.get_object(pk)
        if request.user == answer.answerer:
            answer.delete()
            return Response({'message': 'Answer deleted successfully'})
        else:
            return Response({'message': 'delete not allowed'})

class QuestionSearchView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'body']

    def get_queryset(self):
        query = self.request.GET.get("search")
        vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
        search_query = SearchQuery(query)
        rank = SearchRank(vector, query)
        return Question.objects.annotate(rank=rank).filter(rank__gt=0.3).order_by('-rank')
    
class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    lookup_field = 'slug'