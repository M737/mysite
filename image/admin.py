from django.contrib import admin
from .models import Img

# Register your models here.

@admin.register(Img)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['name', 'img_url']