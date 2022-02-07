from django.db import models
from account.models import MyUser
from taggit.managers import TaggableManager
from django.utils.text import slugify

class Question(models.Model):
    title           = models.CharField(max_length=160)
    slug            = models.CharField(unique=True, max_length=255)
    body            = models.TextField(blank=True)
    created         = models.DateTimeField(auto_now_add=True)
    questioner      = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    upvoters        = models.ManyToManyField(MyUser, related_name='upvotes', blank=True)
    tags            = TaggableManager()
    verified_answer = models.OneToOneField('questions.Answer', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

class Answer(models.Model):
    answerer        = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    question_id     = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    body            = models.TextField()
    created         = models.DateTimeField(auto_now_add=True)
    upvotes         = models.ManyToManyField(MyUser, related_name='upvoters', blank=True)
    downvotes       = models.ManyToManyField(MyUser, related_name='downvoters', blank=True)

    def __str__(self):
        return self.body
    