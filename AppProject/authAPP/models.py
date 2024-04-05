from django.db import models

"""
定义用户模型（或扩展Django提供的默认用户模型），以便存储用户的身份验证信息和其他相关信息。
"""
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """
    在这个用户模型中，CustomUser继承自AbstractUser，并添加了email字段作为用户的电子邮件。followers字段是一个多对多关系字段，用于表示用户的粉丝（关注者），通过related_name='following'指定了反向关系的名称。
    此外，模型中包含了follow、unfollow和is_following方法，用于实现关注和粉丝功能。follow方法用于关注另一个用户，unfollow方法用于取消关注，is_following方法用于检查当前用户是否关注了另一个用户。
    这个用户模型提供了基本的用户信息存储功能，并实现了简单的关注和粉丝功能。你可以根据实际需求和项目的复杂性进行进一步扩展和定制。
    """
    # 添加或修改related_name参数
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_name="customuser_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="customuser_set",
        related_query_name="user",
    )
    email = models.EmailField(unique=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following')

    def follow(self, user):
        if not self.is_following(user):
            self.following.add(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)

    def is_following(self, user):
        return self.following.filter(id=user.id).exists()
