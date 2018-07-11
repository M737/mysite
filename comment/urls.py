from django.urls import path
from . import views

urlpatterns= [
    path('update_comment', views.update_comment, name='update_comment'),
    path('update_message', views.update_message, name='update_message'),
    path('update_remark', views.update_remark, name='update_remark')
]