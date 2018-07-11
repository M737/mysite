from django.shortcuts import render
from django.http import JsonResponse
from .models import LikeCount, LikeRecord
from django.contrib.contenttypes.models import ContentType

# Create your views here.


def SuccessResponse(liked_num):
    data = {}
    data['status'] = 'SUCCESS'
    data['liked_num'] = liked_num
    return JsonResponse(data)

def ErrorResponse(code, message):
    data = {}
    data['status'] = 'Error'
    data['code'] =code
    data['message'] = message
    return JsonResponse(data)

def like_change(request):
    #获取数据
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse(401, 'you were not login')
    content_type = request.GET.get('content_type')
    content_type = ContentType.objects.get(model=content_type)
    object_id = int(request.GET.get('object_id'))
    is_like = request.GET.get('is_like')

    #处理数据
    if is_like == 'true':
        #要点赞
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id , user=user)
        if created:
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id )
            like_count.liked_num += 1
            like_count.save()
            return SuccessResponse(like_count.liked_num)
        else:
            # 已经点赞，不能重复点赞
            return ErrorResponse(402, 'you were liked')

    else:
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            # 有过点赞，取消点赞
            like_record = LikeRecord.objects.get(content_type=content_type,object_id=object_id, user=user)
            like_record.delete()
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id )

            if not created:
                like_count.liked_num -= 1
                like_count.save()
                return SuccessResponse(like_count.liked_num)
            else:
                return ErrorResponse(404, 'data error')
        else:
            # 没有点赞，不能取消
            return ErrorResponse(403,'you were not liked')


