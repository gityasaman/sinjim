from rest_framework import routers
from . import views
from django.urls import path, include

router1 = routers.DefaultRouter()
router2 = routers.DefaultRouter()

router1.register('questions', views.QuestionViewSet)
router2.register('answers', views.AnswerViewSet)

urlpatterns = [
    path('', include(router1.urls)),
    path('', include(router2.urls)),
]
