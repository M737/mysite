from django.contrib.contenttypes.models import ContentType
from django import template
from ..models import LikeRecord,LikeCount

register = template.Library()

@register.simple_tag
def get_content_type(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return content_type.model

@register.simple_tag
def get_like_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=obj.pk)
    return like_count.liked_num

@register.simple_tag(takes_context=True)
def get_like_status(context, obj):
    user = context['user']
    if not user.is_authenticated:
        return ''
    content_type = ContentType.objects.get_for_model(obj)
    like_status = LikeRecord.objects.filter(content_type=content_type, object_id=obj.pk, user=user).exists()
    if like_status:
        return 'active'
    else:
        return ''
