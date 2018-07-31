import random
import string
import traceback
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import JsonResponse

from .form import UserForm, RegisterForm,ForgetPasswordForm, ChangePasswordForm, SelfInfoForm, MoodForm
from .models import Profile, Mood


referer = {}
referer['referer'] = '/'

# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    context = {}
    message = ''
    if request.method =='POST':
        login_form = UserForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = auth.authenticate(username=username,password=password)
            if user is not None:
                request.session['is_login'] = True
                request.session['user_name'] = username
                auth.login(request, user)
                return redirect(referer['referer'])
            else:
                message = '用户名或密码错误'
        else:
            message = '验证码错误'
        context['message'] = message
        context['login_form'] = login_form
        return render(request, 'user/login.html', context)
    else:
        current_referer = request.META.get('HTTP_REFERER', '/')
        if not ('register' in current_referer or 'change_password' in current_referer):
            referer['referer'] = current_referer
    context['login_form'] = UserForm()
    return render(request, 'user/login.html',context)

def logout(request):
    referer = request.META.get('HTTP_REFERER', '/')
    auth.logout(request)
    return redirect(referer)

def register(request):
    context = {}
    message = ''
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            password_repeat = register_form.cleaned_data['password_repeat']
            if password == password_repeat:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect(reverse('login'))
            else:
                message = "两次密码不一致"
        else:
            message = register_form.errors
        context['message'] = message
        context['register_form'] = register_form
        return render(request, 'user/register.html', context)
    else:
        referer['referer'] = request.META.get('HTTP_REFERER', '/')
    context['register_form'] = RegisterForm()
    return render(request, 'user/register.html', context)


def forget_password(request):
    if request.user.is_authenticated:
        return redirect('/')
    context = {}
    if request.method == 'POST':
        forget_password_form = ForgetPasswordForm(request.POST)
        if forget_password_form.is_valid():
            username = forget_password_form.cleaned_data['username']
            email = forget_password_form.cleaned_data['email']
            if User.objects.filter(username=username, email=email).exists():
                request.session['username'] = username
                request.session['email'] = email
                return redirect(reverse('change_password'))
            else:
                message = '用户名或者邮箱错误'
        else:
            message = forget_password_form.errors
        context['message'] = message
        context['forget_password_form'] = forget_password_form
        return render(request, 'user/forget_password.html', context)
    else:
        context['forget_password_form'] = ForgetPasswordForm()
    return  render(request, 'user/forget_password.html', context)


def change_password(request):
    context = {}
    if request.method == 'POST':
        change_password_form = ChangePasswordForm(request.POST)
        if change_password_form.is_valid():
            password = change_password_form.cleaned_data['password']
            password_repeat = change_password_form.cleaned_data['password_repeat']
            if password == password_repeat:
                username = request.session.get('username')
                email = request.session.get('email')
                user = User.objects.get(username=username, email=email)
                user.set_password(password)
                user.save()
                return redirect(reverse('login'))
            else:
                message = "两次密码不一致"
        else:
            message = change_password_form.errors
        context['message'] = message
        context['change_password_form']= change_password_form
    else:
        context['change_password_form'] = ChangePasswordForm()
    return render(request, 'user/change_password.html', context)






@login_required(login_url='/user/login')
def self_info(request):
    context = {}
    user = request.user
    try:
        profile = user.profile
        context['is_created'] = True
        context['photo'] = str(profile.photo)
        context['profile'] = profile
        moods = Mood.objects.filter(profile=profile)
        context['moods'] = moods.order_by('-mood_time')
        context['mood_form'] = MoodForm()
    except:
        print(traceback.print_exc())
        context['is_created'] = False
    return render(request, 'user/self_info.html', context)

def create_self_info(request):
    context = {}
    if request.method == 'POST':
        self_info_form = SelfInfoForm(request.POST)
        if self_info_form.is_valid():
            nickname = self_info_form.cleaned_data['nickname']
            resume = self_info_form.cleaned_data['resume']
            photo = request.FILES.get('photo')
            profile = Profile(user=request.user, nickname=nickname, resume=resume, photo=photo)
            profile.save()
            return redirect(reverse('self_info'))
        else:
            print(self_info_form.errors)
    else:
        context['self_info_form'] = SelfInfoForm()
    return render(request, 'user/create_self_info.html', context)


@login_required(login_url='/user/login')
def change_nickname(request):
    referer = request.META.get('HTTP_REFERER', '/')
    user = request.user
    if request.method =='POST':
        nickname = request.POST.get('nickname')
        profile = Profile.objects.get(user=user)
        profile.nickname = nickname
        profile.save()
        return redirect(referer)
    return render(request,'user/self_info.html')


@login_required(login_url='/user/login')
def change_photo(request):
    referer = request.META.get('HTTP_REFERER', '/')
    user = request.user
    if request.method == 'POST':
        photo = request.FILES.get('photo')
        profile = Profile.objects.get(user=user)
        profile.photo = photo
        profile.save()
        return redirect(referer)
    return render(request, 'user/self_info.html')


@login_required(login_url='/user/login')
def change_resume(request):
    referer = request.META.get('HTTP_REFERER', '/')
    user = request.user
    if request.method == 'POST':
        resume = request.POST.get('resume')
        profile = Profile.objects.get(user=user)
        profile.resume = resume
        profile.save()
        return redirect(referer)
    return render(request, 'user/self_info.html')


@login_required(login_url='/user/login')
def send_code(request):
    email = request.GET.get('email', '')
    data = {}
    if email:
        # 生产验证码
        ver_code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        request.session['ver_code'] = ver_code

        send_mail(
            '绑定邮箱验证码',
            '验证码：{}'.format(ver_code),
            '562729270@qq.com',
            [email],
            fail_silently=False,
        )
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


@login_required(login_url='/user/login')
def bind_email(request):
    referer = request.META.get('HTTP_REFERER', '')
    context = {}
    user = request.user
    if request.method == 'POST':
        email = request.POST.get('email', '')
        code = request.POST.get('captcha', '')
        if code == request.session.get('ver_code'):
            user.email = email
            user.save()
            profile = Profile.objects.get(user=user)
            profile.is_bind = True
            profile.save()
            return redirect(referer)
        else:
            message = '验证码错误'
        context['message'] = message
        return render(request, 'user/self_info.html', context)
    return render(request, 'user/self_info.html')


def write_mood(request):
    referer = request.META.get('HTTP_REFERER', '/')
    user = request.user
    if request.method == 'POST':
        mood_form = MoodForm(request.POST)
        if mood_form.is_valid():
            mood_content = mood_form.cleaned_data['mood_content']
            profile = Profile.objects.get(user=user)
            mood = Mood()
            mood.mood_content = mood_content
            mood.profile = profile
            mood.save()
            return redirect(referer)
        else:
            print(mood_form.errors)
    return render(request, 'user/self_info.html')


