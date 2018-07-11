from django.urls import path
from . import views

urlpatterns= [
    path('', views.word_list, name='word_list'),
    path('create_word_set', views.create_word_set, name='create_word_set'),
    path('update_word_set', views.update_word_set, name='update_word_set'),
    path('modify_word_set/<int:word_set_id>', views.modify_word_set, name='modify_word_set'),
    path('word_set/<int:word_set_id>/', views.word_set, name='word_set'),
    path('memorizing_words/<int:word_set_id>/<int:word_id>', views.memorizing_words, name='memorizing_words'),
    path('content_to_write_word/<int:word_set_id>/<int:word_id>', views.content_to_write_word, name='content_to_write_word'),
    path('word_to_choice_content/<int:word_set_id>/<int:word_id>', views.word_to_choice_content, name='word_to_choice_content'),
]

urlpatterns += [
    path('collector', views.my_collector, name='my_collector'),
    path('create_collector', views.create_collector, name='create_collector'),
    path('collector/<int:collector_id>', views.collector_detail, name='collector_detail'),
    path('add_to_collector/<int:word_id>', views.add_to_collector, name='add_to_collector'),
    path('set_default_collector/<int:collector_id>', views.set_default_collector, name='set_default_collector'),
]