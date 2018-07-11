from django.shortcuts import render, redirect
from .models import Img

# Create your views here.

def upload_img(request):
    context = {}
    message = ''
    referer = request.META.get('HTTP_REFERER', '/')
    if request.method == 'POST':
        try:
            img = Img(img_url=request.FILES.get('img'),
                        name=request.FILES.get('img').name)
            img.save()
            return redirect(referer)
        except:
            massage = '上传失败'
        context['message'] = message
        return render(request, 'image/upload_img.html', context)
    return render(request, 'image/upload_img.html')


def show_img(request):
    context = {}
    imgs = Img.objects.all()
    context['imgs'] = imgs
    return render(request, 'image/show_img.html', context)