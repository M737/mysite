from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Content(models.Model):
    content_name = models.CharField(max_length=200)

    def __str__(self):
        return self.content_name

class WordSet(models.Model):
    set_name = models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)
    create_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.set_name



class Word(models.Model):
    word_name = models.CharField(max_length=50)
    content = models.OneToOneField(Content, on_delete=models.CASCADE)
    word_set = models.ForeignKey(WordSet, on_delete=models.CASCADE)
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.word_name


class Collector(models.Model):
    collector_name = models.CharField(max_length=50)
    collect_time = models.DateTimeField(auto_now_add=True)
    collect_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    word = models.ManyToManyField(Word)

    class Meta:
        ordering = ['-collect_time']

    def __str__(self):
        return self.collector_name








