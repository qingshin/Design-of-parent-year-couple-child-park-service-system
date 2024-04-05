from django.db import models

"""
包含应用程序的数据模型定义，定义了用户模型和其他相关模型。
"""
# Create your models here.
from django.db import models
from django.conf import settings


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
