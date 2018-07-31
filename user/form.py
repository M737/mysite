import re
from django import forms
from captcha.fields import CaptchaField
from django.contrib import auth
from django.contrib.auth.models import User
from ckeditor.widgets import CKEditorWidget

class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码')

    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        if not username:
            raise forms.ValidationError('用户名不允许为空')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password', '')
        if not password:
            raise forms.ValidationError('密码不允许为空')
        return password


class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱", max_length=50, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_repeat =  forms.CharField(label="确认密码", max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码')

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if not username:
            raise forms.ValidationError('用户名不允许为空')
        if len(username) < 4:
            raise forms.ValidationError('用户名需大于4个字符')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已经注册')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password', '').strip()
        if not password:
            raise forms.ValidationError('密码不允许为空')
        if len(password) < 6:
            raise forms.ValidationError('密码长度需大于等于6个字符')
        return password

    def clean_password_repeat(self):
        password_repeat = self.cleaned_data.get('password_repeat', '').strip()
        if not password_repeat:
            raise forms.ValidationError('密码不允许为空')
        return password_repeat

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if not email:
            raise forms.ValidationError('邮箱不能为空')
        return email


class ForgetPasswordForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱", max_length=50, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码',error_messages={'required':'验证码错误'})

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if not username:
            raise forms.ValidationError('用户名不允许为空')
        if len(username) < 4:
            raise forms.ValidationError('用户名需大于4个字符')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名尚未注册')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if not email:
            raise forms.ValidationError('邮箱不能为空')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱尚未注册')
        return email


class ChangePasswordForm(forms.Form):
    password = forms.CharField(label="密码", max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_repeat = forms.CharField(label="确认密码", max_length=20,
                                      widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    def clean_password(self):
        password = self.cleaned_data.get('password', '').strip()
        if not password:
            raise forms.ValidationError('密码不允许为空')
        if len(password) < 6:
            raise forms.ValidationError('密码长度需大于等于6个字符')
        return password



class SelfInfoForm(forms.Form):
    nickname = forms.CharField(label='昵称' ,max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    resume = forms.CharField(label='个人简介', required=False, max_length=5000, widget=forms.Textarea(attrs={'class': 'form-control'}))

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname', '').strip()
        if not nickname:
            raise forms.ValidationError('昵称不能为空')
        return nickname


class MoodForm(forms.Form):
    mood_content = forms.CharField(widget=CKEditorWidget('message'),label='个人简介', max_length=500, )



