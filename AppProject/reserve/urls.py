"""
将视图函数添加到urlpatterns列表中，并为每个URL配置指定了相应的路径和视图函数。这样可以将不同的请求映射到对应的视图函数上，实现各种功能的API
！！！！！在Django项目的settings.py文件中找到INSTALLED_APPS设置，确保auth_app应用程序已添加到INSTALLED_APPS列表中！！！！
"""
from django.urls import path
from . import views

urlpatterns = [
    path('activities/', views.get_activity_list, name='get_activity_list'),
    path('activities/<int:activity_id>/', views.get_activity_detail, name='get_activity_detail'),
    path('reservations/create/', views.create_reservation, name='create_reservation'),
    path('reservations/<int:reservation_id>/', views.get_reservation_detail, name='get_reservation_detail'),
    path('reservations/<int:reservation_id>/cancel/', views.cancel_reservation, name='cancel_reservation'),
    path('activities/create/', views.create_activity, name='create_activity'),
    path('activities/<int:activity_id>/edit/', views.edit_activity, name='edit_activity'),
    path('activities/<int:activity_id>/delete/', views.delete_activity, name='delete_activity'),
    path('reservations/<int:reservation_id>/manage/', views.manage_reservation, name='manage_reservation'),
]

