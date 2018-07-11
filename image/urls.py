from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns= [
    path('upload_img', views.upload_img, name='upload_img'),
    path('show_img', views.show_img, name='show_img'),
]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
