from django.test import TestCase

"""
包含应用程序的单元测试代码，用于测试应用程序的功能和逻辑。
"""
# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Post, Media

User = get_user_model()  # 获取当前项目使用的用户模型


class PublishContentTests(TestCase):

    def setUp(self):
        # 创建一个用户用于测试
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.client.login(username='testuser', password='12345')
        self.publish_url = reverse('publish_content')  # 确保你已经在urls.py中为publish_content视图设置了名为'publish_content'的URL

    def test_publish_text_content(self):
        # 测试发布仅包含文本内容的动态
        response = self.client.post(self.publish_url, {'content': 'This is a test post'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Post.objects.filter(content='This is a test post').exists())

    def test_publish_text_and_media_content(self):
        # 测试发布包含文本和媒体文件的动态
        with open('dynamic/test/image.jpg', 'rb') as file:
            media_file = SimpleUploadedFile(file.name, file.read(), content_type='image/jpeg')
            response = self.client.post(self.publish_url,
                                        {'content': 'This is a test post with media', 'media_files': [media_file]})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Post.objects.filter(content='This is a test post with media').exists())
        self.assertTrue(Media.objects.exists())  # 确认Media实例已创建
