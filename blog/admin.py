from django.contrib import admin
from blog.models import Blogs, BlogType



# Register your models here.

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('type_name',)


@admin.register(Blogs)
class BlogsAdmin(admin.ModelAdmin):
    list_display = ['title', 'blog_type','read_num', 'pub_date', 'modify_date']
    ordering = ('pub_date',)

