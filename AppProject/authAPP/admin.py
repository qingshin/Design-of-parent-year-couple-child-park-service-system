from django.contrib import admin
"""
注册用户模型以便在Django的后台管理界面中管理用户信息。
"""
# Register your models here.
from django.contrib import admin
from .models import CustomUser

admin.site.register(CustomUser)
