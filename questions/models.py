from django.db import models
from account.models import MyUser
from taggit.managers import TaggableManager
from taggit.models import Tag, TagBase, TaggedItemBase, GenericTaggedItemBase
from django.utils.text import slugify
from django.utils.translation import pgettext_lazy
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save

class QuestionTag(TagBase):
    slug = models.SlugField(allow_unicode=True)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

class TaggedQuestion(GenericTaggedItemBase):
    tag = models.ForeignKey(
        QuestionTag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )

class Question(models.Model):
    title           = models.CharField(max_length=160)
    slug            = models.SlugField(unique=True, max_length=255, allow_unicode=True)
    body            = models.TextField(blank=True)
    created         = models.DateTimeField(auto_now_add=True)
    questioner      = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    upvoters        = models.ManyToManyField(MyUser, related_name='upvotes', blank=True)
    tags            = TaggableManager(through=TaggedQuestion)
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
    upvoters        = models.ManyToManyField(MyUser, related_name='answer_upvotes', blank=True)
    downvoters      = models.ManyToManyField(MyUser, related_name='answer_downvotes', blank=True)

    def __str__(self):
        return self.body
