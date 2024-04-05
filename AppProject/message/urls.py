"""
将视图函数添加到urlpatterns列表中，并为每个URL配置指定了相应的路径和视图函数。这样可以将不同的请求映射到对应的视图函数上，实现各种功能的API
！！！！！在Django项目的settings.py文件中找到INSTALLED_APPS设置，确保auth_app应用程序已添加到INSTALLED_APPS列表中！！！！
"""
from django.urls import path
from . import views

urlpatterns = [
    path('send_message/', views.send_message, name='send_message'),
    path('receive_messages/<int:user_id>/', views.receive_messages, name='receive_messages'),
    path('list_messages/', views.list_messages, name='list_messages'),
    path('search_messages/<str:keyword>/', views.search_messages, name='search_messages'),
    path('get_message_detail/<int:message_id>/', views.get_message_detail, name='get_message_detail'),
    path('mark_as_read/<int:message_id>/', views.mark_as_read, name='mark_as_read'),
    path('mark_as_unread/<int:message_id>/', views.mark_as_unread, name='mark_as_unread'),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
    path('recall_message/<int:message_id>/', views.recall_message, name='recall_message'),
]

