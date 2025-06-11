from django.db import models
from django.contrib.auth.models import User


class Words(models.Model):
    english = models.CharField(max_length=30, unique=True)
    turkish = models.CharField(max_length=30)
    in_sentence = models.CharField(max_length=200)
    img = models.ImageField(upload_to='words_imgs/')


class UserWords(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(Words, on_delete=models.CASCADE)
    is_learned = models.BooleanField(default=False)
    corect_count = models.IntegerField(default=0)
    added_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'word')


class QuestionCount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ask_count = models.IntegerField(default=0)
