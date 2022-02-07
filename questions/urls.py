from . import views
from rest_framework import routers
from django.urls import path, include

urlpatterns = [
    path('ask', views.CreateQuestionView.as_view(), name='ask'),
    path('', views.QuestionListView.as_view(), name='questions_list'),
    path('<pk>', views.QuestionDetailView.as_view(), name='question_detail'),
    path('<pk>/upvote', views.UpvoteQuestionView.as_view(), name='upvote'),
    path('<pk>/edit', views.QuestionUpdateView.as_view(), name='edit'),

]
