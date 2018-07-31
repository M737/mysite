from django import forms
from .models import WordSet
from django.forms import widgets

class WordForm(forms.Form):
    placeholder = '单词和释义用两个或两个以上空格分开，支持多行录入，每个单词各占一行，示例：\nclass   n. 班级,(等)阶级,种类 vt. 分类 \nget into  vt. 上（车）,进入(陷入,从事于,研究,习惯于,变成)'
    word_set = forms.CharField(label='创建单词集', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'长度不超过20个字符'}))
    add_word = forms.CharField(label='新增单词', widget=forms.Textarea(attrs={'class': 'form-control', 'rows':"5", 'placeholder':placeholder}), )

    # def clean(self):
    #     word_set = self.cleaned_data['word_set']
    #     add_word = self.cleaned_data['add_word']
    #
    #     return  self.cleaned_data


class WriteForm(forms.Form):
    write_word = forms.CharField(label='拼写单词',widget=forms.TextInput(attrs={'class': 'form-control'}))
    # write_content = forms.CharField(label='单词释义')

class ChoiceForm(forms.Form):
    choice = forms.ChoiceField(widget=widgets.RadioSelect)


class CollectorForm(forms.Form):
    collector_name = forms.CharField(label="创建收藏集", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'长度不超过20个字符'}))
