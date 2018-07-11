from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    comment_text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, related_name='comments', on_delete=models.DO_NOTHING)

    root = models.ForeignKey('self', null=True, related_name='root_comment', on_delete=models.DO_NOTHING)
    parent = models.ForeignKey('self', null=True, related_name='parent_comment', on_delete=models.DO_NOTHING)
    reply_to = models.ForeignKey(User, related_name='replies', null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.comment_text

    class Meta:
        ordering = ['comment_time']


class Message(models.Model):
    message_text = models.TextField()
    message_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, related_name='message', on_delete=models.DO_NOTHING)

    root = models.ForeignKey('self', null=True, related_name='root_message', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, related_name='parent_message', on_delete=models.DO_NOTHING)
    reply_to = models.ForeignKey(User, related_name='message_replies', null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.message_text

    class Meta:
        ordering = ['message_time']


class Remark(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    remark_text = models.TextField()
    remark_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.remark_text

    class Meta:
        ordering = ['remark_time']
