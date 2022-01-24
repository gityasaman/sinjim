from django.contrib import admin
from .models import Answer, Question

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', ]
    list_filter = ('title', 'created')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['body', 'question_id']
