import random
import traceback
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import  JsonResponse

from .models import Word, WordSet, Content, Collector
from .form import WordForm, WriteForm, ChoiceForm, CollectorForm
from comment.models import Remark
from comment.form import RemarkForm

# Create your views here.
per_page_num = 20

choices = ''

record = []

def word_list(request):
    context = {}
    context['word_form'] = WordForm()
    word_sets = WordSet.objects.all()
    if  request.user.is_authenticated:
        context['collector_form'] = CollectorForm()
        collectors = Collector.objects.filter(collect_user=request.user)
        context['collectors'] = collectors
        if not request.session.get('default_collector_id'):
            if collectors.first() is not None:
                request.session['default_collector_id'] = collectors.first().id

    keyword = ''
    context['default_collector_id'] = request.session.get('default_collector_id','')
    if request.method == 'POST':
        keyword = request.POST.get('keyword', '').strip()
        if keyword != '请输入关键字进行搜索':
            word_sets = word_sets.filter(Q(set_name__icontains=keyword)|Q(word__content__content_name__icontains=keyword)|Q(word__word_name__icontains=keyword) )
    context['word_sets'] = word_sets.distinct()
    return render(request, 'word/word_list.html', context)


def word_set(request, word_set_id):
    context = {}
    user = request.user
    words = Word.objects.filter(word_set_id=word_set_id)
    context['word_set_id'] = word_set_id
    context['words'] = words
    context['word_set'] = WordSet.objects.get(pk=word_set_id)
    first_word = words.first()
    last_word = words.last()
    word_ids = [word.id for word in words]
    if first_word:
        context['first_word'] = first_word
        context['last_word'] = last_word
        context['random_word_id'] = random.choice(word_ids)

    if request.user.is_authenticated:
        try:
            first_collector_id = Collector.objects.filter(collect_user=user).first().id
            default_collector_id = request.session.setdefault('default_collector_id', first_collector_id)
            collector = Collector.objects.filter(id=default_collector_id, collect_user=user).first()
            context['collector_word_ids'] = set([word.id for word in collector.word.all()])
        except Exception:
            pass

    item = paginator(request, words, 20)
    context = dict(context, **item)
    return render(request, 'word/word_set.html', context)

def memorizing_cards(request, word_set_id):
    context = {}
    user = request.user
    words = Word.objects.filter(word_set_id=word_set_id)
    context['word_set_id'] = word_set_id
    context['words'] = words
    context['word_set'] = WordSet.objects.get(pk=word_set_id)

    item = paginator(request, words, 10)
    context = dict(context, **item)
    return render(request, 'word/memorizing_cards.html', context)


@login_required(login_url='/user/login')
def update_word_set(request):
    referer = request.META.get('HTTP_REFERER', '/')
    if request.method =='POST':
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
    # else:
    #     context['word_form'] = WordForm()
    return render(request, 'word/word_list.html')


@login_required(login_url='/user/login')
def modify_word_set(request, word_set_id):
    context = {}
    word_set = WordSet.objects.get(pk=word_set_id)
    word_form = WordForm(initial={'word_set': word_set})
    context['word_set'] = word_set
    context['word_form'] = word_form
    return render(request, 'word/modify_word_set.html', context)


def paginator(request,object, per_page_num):
    item = {}
    object = object.order_by('id')
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


def word_detail(request, word_set_id, word_id):
    context = common_util(request, word_set_id, word_id)
    user = request.user
    word = context['word']
    word_content_type = ContentType.objects.get_for_model(word)
    context['remarks'] = Remark.objects.filter(content_type=word_content_type, object_id=word_id)
    context['remark_form'] = RemarkForm(initial={'content_type': word_content_type, 'object_id': word_id})

    if request.user.is_authenticated:
        try:
            first_collector_id = Collector.objects.filter(collect_user=user).first().id
            default_collector_id = request.session.setdefault('default_collector', first_collector_id)
            collector = Collector.objects.filter(id=default_collector_id, collect_user=user).first()
            context['collector_word_ids'] = set([word.id for word in collector.word.all()])
        except Exception:
            print(traceback.print_exc())

    return render(request, 'word/word_detail.html', context)


def memorizing_words(request, word_set_id, word_id):
    context = common_util(request, word_set_id, word_id)
    word = context['word']
    word_content_type = ContentType.objects.get_for_model(word)
    context['remarks'] = Remark.objects.filter(content_type=word_content_type, object_id=word_id)
    context['remark_form'] = RemarkForm(initial={'content_type':word_content_type, 'object_id': word_id})

    return render(request, 'word/memorizing_words.html', context)

def content_to_write_word(request, word_set_id, word_id):
    context = common_util(request, word_set_id, word_id)
    word = context['word']
    temp = list(word.word_name)
    temp[1:-1] = list(map(lambda x: '*', temp[1:-1]))
    context['tips'] = ''.join(temp)
    word_tip = word.word_name
    context['word_length'] = len(word.word_name)
    write_form = WriteForm()
    write_form.fields['write_word'].max_length = context['word_length']
    context['write_form'] = write_form
    return render(request, 'word/content_to_write_word.html', context)


def word_to_choice_content(request, word_set_id, word_id):
    context = common_util(request, word_set_id, word_id)
    word = context['word']
    words = context['words']

    choice_form=ChoiceForm()
    try:
        context['word_ids'].remove(word_id)
        sample = random.sample(context['word_ids'], 3)
        sample.append(word_id)
        random.shuffle(sample)
        sample_words = list(map(lambda x: get_object_or_404(words, pk=x), sample))
        context['sample_words'] = sample_words
        choices = [(sample_words[0].id, sample_words[0].content), (sample_words[1].id, sample_words[1].content),
                   (sample_words[2].id, sample_words[2].content), (sample_words[3].id, sample_words[3].content)]
    except ValueError:
        context['sample_words'] = word
        choices = [(word.id, word.content)]
    choice_form.fields['choice'].choices = choices
    context['choice_form'] = choice_form
    return render(request, 'word/word_to_choice_content.html', context)

@login_required(login_url='/user/login')
def delete_word(request, word_set_id, word_id):
    referer = request.META.get('HTTP_REFERER', '/')
    word_set = WordSet.objects.get(pk=word_set_id)
    words = Word.objects.filter(word_set_id=word_set_id)
    if not request.user == word_set.create_user:
        return redirect(referer)
    word = Word.objects.get(id=word_id, word_set_id=word_set_id)
    word.delete()
    return redirect(referer)



@login_required(login_url='/user/login')
def my_collector(request):
    context = {}
    collectors = Collector.objects.filter(collect_user=request.user)
    context['collectors'] = collectors
    return render(request, 'word/collector.html', context)


@login_required(login_url='/user/login')
def create_collector(request):
    referer = request.META.get('HTTP_REFERER', '/')
    context = {}
    if request.method == 'POST':
        collector_form = CollectorForm(request.POST)
        if collector_form.is_valid():
            user = request.user
            collector_name = collector_form.cleaned_data['collector_name']
            collector = Collector(collector_name=collector_name, collect_user=user)
            collector.save()
            return redirect(referer)
        else:
            print(collector_form.errors)
    else:
        context['collector_form'] = CollectorForm()
    return render(request, 'word/word_list.html', context)


@login_required(login_url='/user/login')
def collector_detail(request, collector_id):
    context = {}
    collector = Collector.objects.get(pk=collector_id)
    words = collector.word.all()
    context['words'] = words
    context['collector'] = collector
    first_word = words.first()
    last_word = words.last()
    word_ids = [word.id for word in words]
    if first_word:
        context['first_word'] = first_word
        context['last_word'] = last_word
        context['random_word_id'] = random.choice(word_ids)
    return render(request, 'word/collector_detail.html', context )


@login_required(login_url='/user/login')
def add_to_collector(request, word_id):
    referer = request.META.get('HTTP_REFERER', '/')
    user = request.user
    word = Word.objects.get(id=word_id)
    try:
        first_collector_id = Collector.objects.filter(collect_user=user).first().id
        default_collector_id = request.session.setdefault('default_collector_id', first_collector_id)
        default_collector = Collector.objects.filter(id=default_collector_id, collect_user=user).first()
        if word_id in set([word.id for word in default_collector.word.all()]):
            word = default_collector.word.get(id=word_id)
            default_collector.word.remove(word)
            return redirect(referer)
        collector = Collector(pk=default_collector.pk, collect_user=user, collector_name=default_collector.collector_name, collect_time=timezone.now())
    except:
        print(traceback.print_exc())
        collector = Collector.objects.create(collect_user=user, collector_name='我的收藏')
    collector.word.add(word)
    collector.save()
    return redirect(referer)

@login_required(login_url='/user/login')
def set_default_collector(request, collector_id):
    referer = request.META.get('HTTP_REFERER', '/')
    request.session['default_collector_id'] = collector_id
    return redirect(referer)

def common_util(request, word_set_id, word_id):
    context = {}
    try:
        word_set = WordSet.objects.get(pk=word_set_id)
        words = Word.objects.filter(word_set_id=word_set_id)
    except:
        word_set = Collector.objects.get(pk=word_set_id)
        words = word_set.word.all()
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



def learning_record(request):
    global record
    word = request.GET.get('word', '')
    record.append(word)
    request.session['record'] = record
    return  JsonResponse({'record': record})

def record_result(request):
    pass


















