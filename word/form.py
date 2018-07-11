from django import forms
from .models import WordSet
from django.forms import widgets

class WordForm(forms.Form):
    word_set = forms.CharField(label='创建单词集')
    add_word = forms.CharField(label='新增单词', widget=forms.Textarea)

    # def clean(self):
    #     word_set = self.cleaned_data['word_set']
    #     add_word = self.cleaned_data['add_word']
    #
    #     return  self.cleaned_data


class WriteForm(forms.Form):
    write_word = forms.CharField(label='拼写单词')
    # write_content = forms.CharField(label='单词释义')


class ChoiceForm(forms.Form):
    choice = forms.ChoiceField(widget=widgets.RadioSelect)


class CollectorForm(forms.Form):
    collector_name = forms.CharField(label="创建收藏集")
