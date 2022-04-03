from . import views
from django.urls import path, include, register_converter
from rest_framework import routers
from sinjim.urls import PersianSlugConverter
    
register_converter(PersianSlugConverter, 'persian_slug')

router = routers.DefaultRouter()
router.register('', views.TagViewSet, basename='tags')

urlpatterns = [
    path('tags/', include(router.urls)),
    path('search', views.QuestionSearchView.as_view(), name='question_search'),
    path('tags/search', views.TagSearchView.as_view(), name='tag_search'),
    path('ask', views.CreateQuestionView.as_view(), name='ask'),
    path('<int:pk>', views.QuestionDetailView.as_view(), name='question_detail'),
    path('<persian_slug:tag_slug>', views.QuestionListView.as_view(), name='questions_by_tag'),
    path('', views.QuestionListView.as_view(), name='questions_list'),
    path('<pk>/upvote', views.UpvoteQuestionView.as_view(), name='upvote'),
    path('<pk>/edit', views.QuestionUpdateView.as_view(), name='edit'),
    path('answer/<pk>', views.AnswerDetailView.as_view(), name='answer_detail'),
    path('answer/<pk>/upvote', views.UpvoteAnswerView.as_view(), name='answer_upvote'),
    path('answer/<pk>/downvote', views.DownvoteAnswerView.as_view(), name='answer_downvote'), 
]

