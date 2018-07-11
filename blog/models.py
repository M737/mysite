from django.db import models
from django.contrib.auth.models import User
# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
class BlogType(models.Model):
    type_name = models.CharField(max_length=30)
    def __str__(self):
        return self.type_name

class Blogs(models.Model):
    title = models.CharField(max_length=100)
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING)
    content = RichTextUploadingField()
    read_num = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    is_original = models.BooleanField(default=True)
    blog_url = models.CharField(max_length=255, null=True, default='')
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pub_date']




