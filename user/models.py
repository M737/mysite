from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20)
    resume = models.CharField(max_length=5000)
    register_time = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='image')
    is_bind = models.BooleanField(default=False)

    def __str__(self):
        return self.nickname

class Mood(models.Model):
    mood_content = RichTextUploadingField(max_length=500)
    mood_time = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.mood_content


