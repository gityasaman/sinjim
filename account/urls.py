from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'account'

router = DefaultRouter()


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
    path('register/', views.EmailView.as_view(), name='register'),
    path('register/code', views.CodeView.as_view(), name='email_code'),
    path('register/continue-register', views.ContinueRegisterView.as_view(), name='continue_register'),
    path('api-token-auth', obtain_auth_token),
    #path('code', views.CodeView.as_view(), name='code')
    #path('register/email/', views.EmailCodeView.as_view(), name='email'),
    #path('users/', views.UserList.as_view(), name='users'),
    #path('users/<pk>/', views.UserDetails.as_view()),
    #path('register/', views.RegisterView.as_view(), name='register'),

]

