from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from .models import Comment, Message, Remark
from .form import CommentForm, MessageForm, RemarkForm
# Create your views here.

def update_comment(request):
    # referer = request.META.get('HTTP_REFERER', '/')
    comment_form = CommentForm(request.POST)
    data = {}
    if comment_form.is_valid():
        user = request.user
        comment_text = comment_form.cleaned_data['comment_text']
        content_type = comment_form.cleaned_data['content_type']
        comment = Comment(user=user, comment_text=comment_text, content_object=content_type)

        parent = comment_form.cleaned_data['parent']
        if not parent is None:
            comment.root = parent.root if not parent.root is None else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()
        data['status'] = 'SUCCESS'
        data['user'] = comment.user.username
        data['comment_time'] = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
        data['comment_text'] = comment.comment_text

        if not parent is None:
            data['reply_to'] = comment.reply_to.username
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if not comment.root is None else ''

    else:
        data['status'] = 'ERROR'
        # return render(request, 'error.html', {'message':'评论失败'})
    return JsonResponse(data)


def update_message(request):
    # referer = request.META.get('HTTP_REFERER', '/')
    message_form = MessageForm(request.POST)
    data = {}
    if message_form.is_valid():
        user = request.user
        text = message_form.cleaned_data['message_text']
        message = Message(user=user, message_text=text)

        parent = message_form.cleaned_data['parent']
        if not parent is None:
            message.root = parent.root if not parent.root is None else parent
            message.parent = parent
            message.reply_to = parent.user
        message.save()
        data['status'] = 'SUCCESS'
        data['user'] = message.user.username
        data['message_time'] = message.message_time.strftime('%Y-%m-%d %H:%M:%S')
        data['message_text'] = message.message_text

        if not parent is None:
            data['reply_to'] = message.reply_to.username
        else:
            data['reply_to'] = ''
        data['pk'] = message.pk
        data['root_pk'] = message.root.pk if not message.root is None else ''
    else:
        data['status'] = 'ERROR'
    # return redirect(referer)
    return JsonResponse(data)


def update_remark(request):
    referer = request.META.get('HTTP_REFERER', '/')
    remark_form = RemarkForm(request.POST)
    if remark_form.is_valid():
        user = request.user
        remark_text = remark_form.cleaned_data['remark_text']
        content_type = remark_form.cleaned_data['content_type']
        remark = Remark(user=user, remark_text=remark_text, content_object=content_type)
        remark.save()
    return redirect(referer)



