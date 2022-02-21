"""sinjim URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, register_converter
from django.urls.converters import SlugConverter
from rest_framework import routers
from questions import views

router = routers.DefaultRouter()
router.register('tags', views.TagViewSet, basename='tags')

class PersianSlugConverter(SlugConverter):
    regex = '[-0123456789-ضصثقفغعهخحجچپشسیبلاتنمکگظطزرذدئوآءإؤژيةۀ]'
register_converter(PersianSlugConverter, 'persian_slug')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls', namespace='account')),
    path('questions/', include('questions.urls')),
    path('', include(router.urls)),
]