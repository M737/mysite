import random
import traceback
from pyquery import PyQuery as pq
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from .models import Word, WordSet, Content, Collector
from .form import WordForm, WriteForm, ChoiceForm, CollectorForm
from comment.models import Remark
from comment.form import RemarkForm

# Create your views here.
per_page_num = 20

choices = ''

def word_list(request):
    context = {}
    word_sets = WordSet.objects.all()
    if  request.user.is_authenticated:
        context['collectors'] = Collector.objects.filter(collect_user=request.user)
    keyword = ''
    if request.method == 'POST':
        keyword = request.POST.get('keyword', '').strip()
        if keyword != '请输入关键字进行搜索':
            word_sets = word_sets.filter(Q(set_name__icontains=keyword)|Q(word__content__content_name__icontains=keyword)|Q(word__word_name__icontains=keyword) )
    context['word_sets'] = word_sets.distinct()
    return render(request, 'word/word_list.html', context)

def word_set(request, word_set_id):
    context = {}
    words = Word.objects.filter(word_set_id=word_set_id)
    context['word_set_id'] = word_set_id
    context['words'] = words
    first_word = words.first()
    last_word = words.last()
    word_ids = [word.id for word in words]
    if first_word:
        context['first_word'] = first_word
        context['last_word'] = last_word
        context['random_word_id'] = random.choice(word_ids)

    if request.user.is_authenticated:
        try:
            collector = Collector.objects.filter(id=request.session.setdefault('default_collect_id', 1), collect_user=request.user).first()
            context['collector_word_ids'] = set([word.id for word in collector.word.all()])
        except Exception:
            print(traceback.print_exc())

    item = paginator(request, words)
    context = dict(context, **item)
    return render(request, 'word/word_set.html', context)

@login_required(login_url='/login')
def create_word_set(request):
    context = {}
    word_form = WordForm()
    context['word_form'] = word_form
    # if request.method == 'POST':
    return render(request, 'word/create_word_set.html', context)

@login_required(login_url='/login')
def update_word_set(request):
    referer = request.META.get('HTTP_REFERER', '/')
    word_form = WordForm(request.POST)
    if word_form.is_valid():
        user = request.user
        word_set_name = word_form.cleaned_data['word_set']
        try:
            word_set = WordSet.objects.get(set_name=word_set_name)
        except:
            word_set = WordSet(create_user=user, set_name=word_set_name)
            word_set.save()
        words_and_contents = word_form.cleaned_data['add_word']
        for line in words_and_contents.strip().split('\n'):
            word_and_content = line.replace('：', ':').split('  ', 1)
            if len(word_and_content) == 2:
                word_name = word_and_content[0]
                content_name = word_and_content[1]
                content = Content(content_name=content_name)
                content.save()
                word = Word(word_name=word_name, content=content, word_set=word_set)
                word.save()
        return redirect(referer)
    return render(request, 'word/create_word_set.html')

@login_required(login_url='/login')
def modify_word_set(request, word_set_id):
    context = {}
    word_set = WordSet.objects.filter(pk=word_set_id)
    word_form = WordForm(initial={'word_set': word_set.first()})
    context['word_set'] = word_set
    context['word_form'] = word_form
    return render(request, 'word/modify_word_set.html', context)

def paginator(request,object):
    item = {}
    paginator = Paginator(object, per_page_num)
    page = request.GET.get('page')
    word_pages = paginator.get_page(page)
    current_page_num = word_pages.number
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
    item['word_pages'] = word_pages
    item['page_range'] =page_range
    return item

def memorizing_words(request, word_set_id, word_id):
    context = common_util(request, word_set_id, word_id)
    word = context['word']
    url = "http://apii.dict.cn/mini.php?q={}".format(word.word_name)
    context['word_html'] = pq(url=url, encoding='gb2312').html()

    word_content_type = ContentType.objects.get_for_model(word)
    context['remarks'] = Remark.objects.filter(content_type=word_content_type, object_id=word_id)
    context['remark_form'] = RemarkForm(initial={'content_type':word_content_type, 'object_id': word_id})

    return render(request, 'word/memorizing_words.html', context)

def content_to_write_word(request, word_set_id, word_id):
    context = common_util(request, word_set_id, word_id)
    word = context['word']

    write_form = WriteForm(request.POST)
    if write_form.is_valid():
        write_word = write_form.cleaned_data['write_word']
        if write_word == word.word_name:
            message = '你很棒哟'
            is_correct = 1
        else:
            message = '再考虑考虑'
            is_correct = 0
        context['message'] = message
        context['is_correct'] = is_correct
    context['write_form'] = WriteForm()
    return render(request, 'word/content_to_write_word.html', context)

def word_to_choice_content(request, word_set_id, word_id):
    context = common_util(request, word_set_id, word_id)
    word = context['word']
    words = context['words']

    try:
        sample = random.sample(context['word_ids'], 3)
        sample.append(word.id)
        random.shuffle(sample)
        sample_words = list(map(lambda x:get_object_or_404(words, pk=x), sample))
        context['sample_words'] = sample_words
        choices = [(sample_words[0].id, sample_words[0].content),(sample_words[1].id, sample_words[1].content),(sample_words[2].id, sample_words[2].content),(sample_words[3].id, sample_words[3].content)]
    except ValueError:
        context['sample_words'] = word
        choices = [(word.id,word.content)]

    choice_form = ChoiceForm(request.POST)
    if choice_form.is_valid():
        choice_id = choice_form.cleaned_data['choice']
        if choice_id  == word.id:
            message = '你很棒哟'
            is_correct = 1
        else:
            message = '再考虑考虑'
            is_correct = 0
        context['message'] = message
        context['is_correct'] = is_correct

    choice_form=ChoiceForm()
    choice_form.fields['choice'].choices = choices
    context['choice_form'] = choice_form
    return render(request, 'word/word_to_choice_content.html', context)

@login_required(login_url='/login')
def my_collector(request):
    context = {}
    collectors = Collector.objects.filter(collect_user=request.user)
    context['collectors'] = collectors
    return render(request, 'word/collector.html', context)

@login_required(login_url='/login')
def create_collector(request):
    context = {}
    collector_form = CollectorForm(request.POST)
    if collector_form.is_valid():
        user = request.user
        collector_name = collector_form.cleaned_data['collector_name']
        collector = Collector(collector_name=collector_name, collect_user=user)
        collector.save()
    else:
        print(collector_form.errors)
    context['collector_form'] = CollectorForm()
    return render(request, 'word/create_collector.html', context)

@login_required(login_url='/login')
def collector_detail(request, collector_id):
    context = {}
    collector = Collector.objects.get(pk=collector_id)
    context['words'] = collector.word.all()
    context['collector'] = collector
    return render(request, 'word/collector_detail.html', context )


@login_required(login_url='/login')
def add_to_collector(request, word_id):
    referer = request.META.get('HTTP_REFERER', '/')
    user = request.user
    word = Word.objects.get(id=word_id)
    try:
        default_collector = Collector.objects.filter(id=request.session.setdefault('default_collect_id', 1),collect_user=request.user).first()
        if word_id in set([word.id for word in default_collector.word.all()]):
            word = default_collector.word.get(id=word_id)
            default_collector.word.remove(word)
            return redirect(referer)
        collector = Collector(pk=default_collector.pk, collect_user=user, collector_name=default_collector.collector_name, collect_time=timezone.now())
    except:
        collector = Collector.objects.create(collect_user=user, collector_name='我的收藏')
    collector.word.add(word)
    collector.save()
    return redirect(referer)

@login_required(login_url='/login')
def set_default_collector(request, collector_id):
    referer = request.META.get('HTTP_REFERER', '/')
    request.session['default_collect_id'] = collector_id
    return redirect(referer)

def common_util(request, word_set_id, word_id):
    context = {}
    word_set = WordSet.objects.get(pk=word_set_id)
    words = Word.objects.filter(word_set_id=word_set_id)
    context['words'] = words
    word = get_object_or_404(words, pk=word_id)
    context['word'] = word
    context['word_set'] = word_set
    first_word = words.first()
    last_word = words.last()
    word_ids = [word.id for word in words]
    context['word_ids'] = word_ids
    word_index = word_ids.index(word_id)
    if first_word:
        context['first_word'] = first_word
        context['last_word'] = last_word
        context['random_word_id'] = random.choice(word_ids)
        context['previous_word_id'] = first_word.id if word_id == first_word.id else word_ids[word_index - 1]
        context['next_word_id'] = last_word.id if word_id == last_word.id else word_ids[word_index + 1]
    return context















