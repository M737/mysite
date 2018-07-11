from django.contrib import admin
from .models import Comment, Message, Remark


# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'content_object','comment_text', 'comment_time')
    ordering = ['-comment_time']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'message_text', 'message_time']
    ordering = ['-message_time']


@admin.register(Remark)
class RemarkAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'remark_text', 'remark_time']
    ordering = ['-remark_time']