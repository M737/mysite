from django.shortcuts import render
from blog.models import Blogs
from comment.form import MessageForm
from comment.models import Message
from blog.views import paginator
from user.form import UserForm, RegisterForm



def home(request):
    context = {}
    blogs = Blogs.objects.all()
    context['blogs'] = blogs
    context['login_form'] = UserForm

    return render(request, 'home.html',context)



def leave_message(request):
    context = {}
    context['message_form'] = MessageForm(initial={'reply_message_id':0})
    messages = Message.objects.filter(parent=None)
    context['messages'] = messages.order_by('-message_time')
    item = paginator(request, context['messages'])
    context = dict(context, **item)
    return render(request, 'leave_message.html', context)