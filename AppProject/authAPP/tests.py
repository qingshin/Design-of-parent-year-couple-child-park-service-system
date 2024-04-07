from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

"""
包含应用程序的单元测试代码，用于测试应用程序的功能和逻辑。
"""


class UserRegisterTestCase(TestCase):
    """
    测试用户注册功能的单元测试类
    """

    def setUp(self):
        self.register_url = reverse('user_register')  # 假设你的注册视图的URL名称为'user_register'
        self.user_model = get_user_model()

    def test_register_success(self):
        # 测试成功注册
        response = self.client.post(self.register_url, {
            'username': 'user1',
            'email': 'user1@example.com',
            'password': '12345'
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'message': 'User registered successfully'})
        # 确认用户确实被创建
        self.assertTrue(self.user_model.objects.filter(username='user1').exists())

    def test_register_failure_missing_fields(self):
        # 测试注册时缺少必要信息
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            # 密码缺失
        })
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(str(response.content, encoding='utf8'),
                             {'error': 'Please provide username, email, and password'})

    def test_register_failure_username_exists(self):
        # 测试使用已存在的用户名注册
        existing_user = self.user_model.objects.create_user(username='testuser', email='11@qq.com',
                                                            password='666666')
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'email': '11@qq.com',
            'password': '666666'
        })
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'error': 'Username already exists'})


# Create your tests here.
class UserLoginTestCase(TestCase):
    """
    测试用户登录功能的单元测试类
    """

    def setUp(self):
        # 创建一个测试用户
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='666666')
        self.login_url = reverse('user_login')  # 假设你的登录视图的URL名称为'user_login'

    def test_login_success(self):
        # 测试使用有效凭据登录
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': '666666'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'message': 'Login successful'})

    def test_login_failure(self):
        # 测试使用无效凭据登录
        response = self.client.post(self.login_url,
                                    {'username': 'testuser', 'password': 'wrongpassword'})  # 使用错误的密码尝试登录
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'message': 'Login failed'})


class UserLogoutTest(TestCase):
    """
    用户登出测试
    """

    def setUp(self):
        # 创建一个用户用于登录和登出测试
        User_test = get_user_model()  # 使用get_user_model()函数获取默认的用户模型类
        self.user = User_test.objects.create_user(username='testuser',email='testuser@example.com', password='123456')
        self.client = Client()
        # 登录用户
        self.client.login(username='testuser', password='123456')

    def test_logout(self):
        # 获取登出视图的URL
        url = reverse('user_logout')  # 假设你的登出视图的URL名称为'logout'
        # 发送POST请求到登出视图
        response = self.client.post(url)
        # 验证返回的状态码是否为200（成功）
        self.assertEqual(response.status_code, 200)
        # 验证返回的JSON消息
        self.assertEqual(response.json(), {'message': 'User logged out successfully'})


class GetUserInfoTestCase(TestCase):
    """
    获取用户信息测试
    """

    def setUp(self):
        # 创建两个测试用户
        User = get_user_model()
        self.user1 = User.objects.create_user(username='不存在的用户', email='00@qq.com', password='123456')
        self.user2 = User.objects.create_user(username='testuser', email='testuser@example.com', password='666666',
                                              is_staff=True)

    def test_get_user_info_success(self):
        # 测试获取存在用户的信息
        url = reverse('get_user_info', kwargs={'user_id': self.user1.id})  # 假设你的视图的URL名称为'get_user_info'
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'username': self.user1.username,
            'email': self.user1.email,
            'is_staff': self.user1.is_staff,
            'is_active': self.user1.is_active
        })

    def test_get_user_info_not_found(self):
        # 测试获取不存在用户的信息
        non_existing_user_id = self.user1.id + self.user2.id + 1  # 假设这个ID不存在
        url = reverse('get_user_info', kwargs={'user_id': non_existing_user_id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'error': 'User not found'})


class UserRelationshipTestCase(TestCase):
    """
    用户关系测试,即获取关注列表和粉丝列表的测试
    """

    def setUp(self):
        # 创建测试用户
        User_test = get_user_model()
        self.user1 = User_test.objects.create_user(username='user1', email='user1@example.com', password='12345')
        self.user2 = User_test.objects.create_user(username='user2', email='user2@example.com', password='12345')
        # 假设有方法来设置用户之间的关注关系
        # 例如，
        self.user1.follow(self.user2)  # user1 关注了 user2
        # 注意：你需要根据你的模型实际情况来调整这部分代码

    def test_get_following_users(self):
        # 测试获取关注的用户列表
        url = reverse('get_following_users', kwargs={'user_id': self.user1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        expected_response = [{'username': self.user2.username, 'email': self.user2.email}]
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_response)

    def test_get_followers(self):
        # 测试获取粉丝列表
        url = reverse('get_followers', kwargs={'user_id': self.user2.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        expected_response = [{'username': self.user1.username, 'email': self.user1.email}]
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_response)

    def test_user_not_found(self):
        # 测试用户不存在的情况
        non_existing_user_id = self.user1.id + self.user2.id + 1
        url = reverse('get_following_users', kwargs={'user_id': non_existing_user_id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'error': 'User not found'})
