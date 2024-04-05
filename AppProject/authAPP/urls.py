from django.urls import path
from .views import user_login, user_register, user_logout, get_user_info, get_following_users, get_followers, \
    login_test_page, register_test_page

"""
将视图函数添加到urlpatterns列表中，并为每个URL配置指定了相应的路径和视图函数。这样可以将不同的请求映射到对应的视图函数上，实现各种功能的API
！！！！！在Django项目的settings.py文件中找到INSTALLED_APPS设置，确保auth_app应用程序已添加到INSTALLED_APPS列表中！！！！
"""
urlpatterns = [
    path('register/', user_register, name='user_register'),
    path('regtest/', register_test_page, name='login_test_page'),  # 注册测试页面
    path('login/', user_login, name='user_login'),
    path('login-test/', login_test_page, name='login_test_page'),
    path('logout/', user_logout, name='user_logout'),
    path('user/<int:user_id>/', get_user_info, name='get_user_info'),  # 获取用户信息
    path('user/<int:user_id>/following/', get_following_users, name='get_following_users'),  # 获取用户的关注列表
    path('user/<int:user_id>/followers/', get_followers, name='get_followers'),  # 获取用户的粉丝列表

]
