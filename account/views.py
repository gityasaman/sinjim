from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from rest_framework import generics, permissions, status, viewsets, mixins
from .serializers import  EmailSerializer, CodeSerializer
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from . import methods
from django.conf import settings
import random
import redis
from django.conf import settings
import hashlib

r = redis.StrictRedis(host=settings.REDIS_HOST,
                                  port=settings.REDIS_PORT, db=0)

# Create your views here.
# class UserList(generics.ListCreateAPIView):
#     permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class UserDetails(generics.RetrieveAPIView):
#     permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#     def post(self, request, format=None):
#         serializer = ProfileSerializer(data=request.data)
#         data = {}
#         if serializer.is_valid():
#             profile = serializer.save()
#             data['avatar'] = profile.avatar
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):

    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            profile = Profile.objects.create(user=user)
            data['response'] = 'Successfully registered'
            data['email'] = user.email
            data['username'] = user.username
            data['avatar'] = user.avatar
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

               
    

class EmailView(APIView):
    serializer_class = EmailSerializer

    def post(self, request, format=None):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            code = methods.generate_code()
            email = serializer.validated_data['email']
            request.session['email'] = email
            r.set(email, code)
            r.expire(email, 300)
            if r.exists(email):
                methods.send_verification_mail(email, code)
                return HttpResponseRedirect('code')

        else:
            return serializer.errors


class CodeView(APIView):
    serializer_class = CodeSerializer

    def post(self, request, format=None):
        serializer = CodeSerializer(data=request.data)
        
        if serializer.is_valid():
            email = request.session['email']
            redis_code = r.get(email)  #Get the verification code from redis
            redis_code = redis_code.decode("utf-8")  #delete the b'' from the string
            if  serializer.validated_data['code'] == redis_code:
                return HttpResponseRedirect('continue_register') 
            else:
                return Response({"message":'codes does not match'})
        else:
            return serializer.errors

