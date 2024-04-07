from django.db import models

"""
包含应用程序的数据模型定义，定义了用户模型和其他相关模型。
"""
# Create your models here.
from django.conf import settings
from django.db import models

"""
首先，我们定义一个Post模型，它将包含动态的基本信息，如文本内容、发布时间和关联的用户。
为了支持未来可能的多媒体内容，我们可以创建一个Media模型，用于存储媒体文件的相关信息，如文件类型、文件路径等。
这样，每个Post可以关联多个Media对象，从而支持文本+图片/视频等多种形式的动态。
"""

"""
用户关联：Post模型通过ForeignKey与Django内置的User模型关联，这样每个动态都与发布它的用户相关联。
动态内容：Post模型的content字段用于存储动态的文本内容。它允许为空，因为假设用户可能只发布媒体内容而不包含文本。
媒体关联：Media模型通过ForeignKey与Post模型关联，允许一个动态关联多个媒体文件。这种设计支持将来对动态内容类型的扩展。
媒体类型和路径：Media模型包含media_type和file_path字段，分别用于存储媒体文件的类型（如图片或视频）和文件路径。
"""


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Post {self.id} by {self.user}'


class Media(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media')
    media_type = models.CharField(max_length=50)  # 例如 'image', 'video'
    file_path = models.FileField(upload_to='media/')  # 假设所有媒体文件都保存在media目录下
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Media {self.id} for Post {self.post_id}'


class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.id}'
