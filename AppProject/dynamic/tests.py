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
from django.utils import timezone

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


class EditContentTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='12345')
        self.other_user = User.objects.create_user(username='otheruser', email='otheruser@example.com',
                                                   password='12345')
        self.client = Client()
        self.client.login(username='testuser', password='12345')
        self.post = Post.objects.create(user=self.user, content='Original content')
        self.edit_url = reverse('edit_content', kwargs={'content_id': self.post.id})

    def test_edit_content_success(self):
        # 测试成功更新内容
        response = self.client.post(self.edit_url, {'content': 'Updated content'})
        self.post.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.post.content, 'Updated content')

    def test_edit_content_no_content_provided(self):
        # 测试没有提供新内容的情况
        response = self.client.post(self.edit_url, {})
        self.assertEqual(response.status_code, 400)

    def test_edit_content_not_owner(self):
        # 测试非发布者尝试编辑内容
        self.client.logout()
        self.client.login(username='otheruser', password='12345')
        response = self.client.post(self.edit_url, {'content': 'Malicious update'})
        self.assertEqual(response.status_code, 404)


class DeleteContentTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='12345')
        self.other_user = User.objects.create_user(username='otheruser', email='otheruser@example.com',
                                                   password='12345')
        self.client = Client()
        self.client.login(username='testuser', password='12345')
        self.post = Post.objects.create(user=self.user, content='A post to be deleted')
        self.delete_url = reverse('delete_content', kwargs={'content_id': self.post.id})

    def test_delete_content_success(self):
        # 测试成功删除动态
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_delete_content_not_found(self):
        # 测试尝试删除不存在的动态
        wrong_url = reverse('delete_content', kwargs={'content_id': 9999})
        response = self.client.delete(wrong_url)
        self.assertEqual(response.status_code, 404)

    def test_delete_content_not_owner(self):
        # 测试非发布者尝试删除动态
        self.client.logout()
        self.client.login(username='otheruser', password='12345')
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, 403)


class ListContentTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.list_content_url = reverse('list_content')
        # 创建测试用户
        self.user = User.objects.create_user(username='testuser', password='12345')
        # 创建测试动态和媒体文件
        for i in range(15):  # 创建15个动态以测试分页
            post = Post.objects.create(user=self.user, content=f'Post {i}', created_at=timezone.now())
            Media.objects.create(post=post, media_type='image', file_path=f'dynamic/test/image.jpg')

    def test_list_content_status_code(self):
        # 测试视图返回的状态码是否为200
        response = self.client.get(self.list_content_url)
        self.assertEqual(response.status_code, 200)

    def test_list_content_pagination(self):
        # 测试分页功能，确保第一页返回10个动态
        response = self.client.get(self.list_content_url)
        self.assertEqual(len(response.json()['posts']), 10)
        # 测试请求第二页
        response = self.client.get(self.list_content_url, {'page': 2})
        self.assertEqual(len(response.json()['posts']), 5)  # 因为总共有15个动态

    def test_list_content_order(self):
        # 测试动态是否按创建时间降序排序
        response = self.client.get(self.list_content_url)
        posts = response.json()['posts']
        self.assertTrue(all(posts[i]['created_at'] >= posts[i + 1]['created_at'] for i in range(len(posts) - 1)))

    def test_list_content_media_files(self):
        # 测试动态是否包含媒体文件信息
        response = self.client.get(self.list_content_url)
        posts = response.json()['posts']
        for post in posts:
            self.assertTrue('media' in post)
            self.assertTrue(len(post['media']) > 0)  # 假设每个动态至少有一个媒体文件


class GetContentDetailTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(user=self.user, content='A detailed post', created_at=timezone.now())
        Media.objects.create(post=self.post, media_type='image', file_path='/path/to/image.jpg')
        self.detail_url = reverse('get_content_detail', kwargs={'content_id': self.post.id})

    def test_get_content_detail(self):
        # 测试获取动态详情
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], self.post.id)
        self.assertEqual(response.json()['user'], self.user.username)
        self.assertEqual(response.json()['content'], 'A detailed post')
        self.assertTrue('media' in response.json())
        self.assertEqual(len(response.json()['media']), 1)
