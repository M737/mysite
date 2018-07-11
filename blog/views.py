from django.shortcuts import render, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.db.models import Q
from blog.models import Blogs, BlogType
from comment.form import CommentForm
from comment.models import Comment, Message
# Create your views here.
per_page_num = 4

def blog_list(request):
    context = {}
    blogs = Blogs.objects.all()
    context['blogs_count'] = len(blogs)
    keyword = ''
    if request.method == 'POST':
        keyword = request.POST.get('keyword', '').strip()
        if keyword != '请输入关键字进行搜索':
            blogs = blogs.filter(Q(title__icontains=keyword)|Q(content__icontains=keyword))
    context['blogs']= blogs
    context['keyword'] = keyword
    comments = Comment.objects.all()
    context['comments'] = comments
    context['last_comments'] = comments[0:5] if len(comments)>5 else comments
    messages = Message.objects.all()
    context['messages'] = messages
    context['last_messages'] = messages[0:5] if len(messages)>5 else messages
    users = User.objects.all()
    context['users'] = users
    try:
        context['author'] = users[0]
    except IndexError:
        context['author'] = '暂未创建'
    blog_types = BlogType.objects.all()

    # 博客类型数量
    blog_type_length_list = []
    for blog_type in blog_types:
        blog_with_type = get_object_or_404(BlogType, pk=blog_type.pk)
        blog_type_length = len(Blogs.objects.filter(blog_type=blog_with_type))
        blog_type_length_list.append(blog_type_length)
    context['blog_type_and_length'] = zip(blog_types, blog_type_length_list)

    # 获取博客评论数
    blog_comments_num_list = []
    for blog in blogs:
        blog_with_comments = get_object_or_404(Blogs, pk=blog.pk)
        blog_content_type = ContentType.objects.get_for_model(blog_with_comments)
        comments_filter = Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk, parent=None)
        blog_comments_num_list.append(comments_filter)
    comment_paginator = Paginator(blog_comments_num_list, per_page_num)
    page = request.GET.get('page')
    comments_page = comment_paginator.get_page(page)

    # 分割页面，设置翻页
    item = paginator(request, blogs)
    context = dict(context, **item)
    context['blog_pages_and_comments_nums'] = zip(context['blog_pages'], comments_page)
    return render(request, 'blog/blog_list.html', context)

def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blogs, pk=blog_pk)
    blog_content_type = ContentType.objects.get_for_model(blog)
    comments = Comment.objects.filter(content_type=blog_content_type, object_id=blog_pk, parent=None)

    if not request.COOKIES.get('blog_{}_read'.format(blog_pk)):
        blog.read_num += 1
        blog.save()

    context = {}
    context['blog'] = blog
    context['user'] = request.user
    context['previous_blog'] = Blogs.objects.filter(pub_date__gt=blog.pub_date).last()
    context['next_blog'] = Blogs.objects.filter(pub_date__lt=blog.pub_date).first()
    context['comments'] = comments.order_by('-comment_time')
    context['comment_form'] = CommentForm(initial={'content_type':blog_content_type, 'object_id':blog_pk, 'reply_comment_id':0})
    response =  render(request, 'blog/blog_detail.html', context)

    response.set_cookie(key='blog_{}_read'.format(blog_pk), value='true', )
    return response

def blog_type(request, blog_type_pk):
    context = {}
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs = Blogs.objects.filter(blog_type=blog_type)
    context['blogs'] = blogs
    context['blog_type'] = blog_type
    # context['contact'] = paginator(request, blogs)
    item = paginator(request, blogs)
    context = dict(context, **item)
    return  render(request, 'blog/blog_type.html', context)

def paginator(request,object):
    item = {}
    paginator = Paginator(object, per_page_num)
    page = request.GET.get('page')
    blog_page = paginator.get_page(page)
    current_page_num = blog_page.number
    page_range = list(range(max(current_page_num-2, 1), current_page_num)) + \
        list(range(current_page_num, min(current_page_num+2, paginator.num_pages)+1))

    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >=2:
        page_range.append('...')
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    item['paginator'] = paginator
    item['blog_pages'] = blog_page
    item['page_range'] =page_range
    return item

