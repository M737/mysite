from django.contrib import admin
from .models import WordSet, Content, Word, Collector

# Register your models here.
@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ['id', 'word_name', 'content', 'word_set', 'add_time']
    ordering = ['-add_time']

@admin.register(WordSet)
class WordSetAdmin(admin.ModelAdmin):
    list_display = ['id', 'set_name', 'create_time', 'create_user']
    ordering = ['-create_time']


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ['content_name']

@admin.register(Collector)
class CollectorAdmin(admin.ModelAdmin):
    list_display = ['id', 'collector_name', 'collect_time', 'collect_user']
    ordering = ['-collect_time']







