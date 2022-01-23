from django.db import models
from taggit.managers import TaggableManager

class Question(models.Model):
    title           = models.CharField(max_length=160)
    slug            = models.CharField(unique=True, max_length=255)
    body            = models.TextField(blank=True)
    created         = models.DateTimeField(auto_now_add=True)
    questioner      = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    verified_answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    upvotes         = models.IntegerField()
    tags            = TaggableManager()

    def __str__(self):
        return self.title

class Answer(models.Model):
    answerer        = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    question_id     = models.ForeignKey(Question, on_delete=models.CASCADE)
    body            = models.TextField()
    created         = models.DateTimeField(auto_now_add=True)
    upvotes         = models.IntegerField()