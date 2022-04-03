from django.contrib import admin
from .models import Answer, Question, QuestionTag, TaggedQuestion

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', ]
    list_filter = ('title', 'created')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['body', 'question_id']

class TaggedItemInline(admin.StackedInline):
    model = TaggedQuestion

@admin.register(QuestionTag)
class QuestionTagAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline]
    list_display = ["name", "slug"]
    ordering = ["name", "slug"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ["name"]}