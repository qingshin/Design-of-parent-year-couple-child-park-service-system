from django.test import TestCase
from django.urls import reverse
from .models import Message
from django.contrib.auth import get_user_model
import json

User = get_user_model()


class MessageTestCase(TestCase):
    def setUp(self):
        # 创建用户实例
        self.user_alice = User.objects.create_user(username='Alice', email='Alice@example.com', password='12345')
        self.user_bob = User.objects.create_user(username='Bob', email='Bob@example.com', password='12345')
        self.user_charlie = User.objects.create_user(username='Charlie', email='Charlie@example.com', password='12345')

        # 直接使用用户实例创建测试消息
        self.message1 = Message.objects.create(sender=self.user_alice, receiver=self.user_bob, content="Hello Bob!")
        self.message2 = Message.objects.create(sender=self.user_bob, receiver=self.user_alice, content="Hi Alice!")


class SendMessageTest(MessageTestCase):
    def test_send_message(self):
        url = reverse('send_message')
        data = {
            'sender': self.user_alice.id,  # 发送用户ID
            'receiver': self.user_bob.id,  # 接收用户ID
            'content': 'Hello Bob!'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Message.objects.count(), 3)
        sent_message = Message.objects.first()
        self.assertEqual(sent_message.content, 'Hello Bob!')
        self.assertEqual(sent_message.sender, self.user_alice)
        self.assertEqual(sent_message.receiver, self.user_bob)


class ReceiveMessagesTest(MessageTestCase):
    def test_receive_messages(self):
        user_id = self.user_bob.id
        url = reverse('receive_messages', args=[user_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(any('Hello Bob!' in message['content'] for message in response_data))


class ListMessagesTest(MessageTestCase):
    def test_list_messages(self):
        url = reverse('list_messages')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_content = response.content.decode()
        self.assertIn('Hello Bob!', response_content)
        self.assertIn('Hi Alice!', response_content)


class SearchMessagesTest(MessageTestCase):
    def test_search_messages(self):
        keyword = 'Hello'
        url = reverse('search_messages', args=[keyword])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Hello Bob!", response.content.decode())


class GetMessageDetailTest(MessageTestCase):
    def test_get_message_detail(self):
        url = reverse('get_message_detail', args=[self.message1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class MarkAsReadTest(MessageTestCase):
    def test_mark_as_read(self):
        url = reverse('mark_as_read', args=[self.message1.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)


class DeleteMessageTest(MessageTestCase):
    def test_delete_message(self):
        url = reverse('delete_message', args=[self.message1.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Message.objects.count(), 1)  # 一个已被删除
