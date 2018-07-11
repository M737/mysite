from django.urls import path
from . import views

urlpatterns= [
    path('', views.grid_system, name='grid_system'),
    path('<int:width>', views.grid_with_width, name='grid_with_width'),
]