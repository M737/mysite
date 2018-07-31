from django.urls import path
from django.conf.urls.static import  static
from django.conf import settings
from . import views

urlpatterns= [
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('forget_password', views.forget_password, name='forget_password'),
    path('change_password', views.change_password, name='change_password'),
    path('self_info', views.self_info, name='self_info'),
    path('create_self_info', views.create_self_info, name='create_self_info'),
    path('change_nickname', views.change_nickname, name='change_nickname'),
    path('change_photo', views.change_photo, name='change_photo'),
    path('change_resume', views.change_resume, name='change_resume'),
    path('send_code', views.send_code, name='send_code'),
    path('bind_email', views.bind_email, name='bind_email'),
    path('write_mood', views.write_mood, name='write_mood'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)