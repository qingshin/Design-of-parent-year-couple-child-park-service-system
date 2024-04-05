from django.contrib.auth import get_user_model
from django.core.serializers.json import DjangoJSONEncoder
from django.forms import model_to_dict
from django.shortcuts import render

"""
包含应用程序的视图函数，处理请求并返回响应，实现应用程序的业务逻辑。
"""
# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Message  # 确保从你的models.py中导入Message模型
from django.core.serializers import serialize
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404


@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        sender_id = request.POST.get('sender')
        receiver_id = request.POST.get('receiver')
        content = request.POST.get('content')

        sender = get_object_or_404(get_user_model(), id=sender_id)
        receiver = get_object_or_404(get_user_model(), id=receiver_id)

        # 使用Django模型创建新消息
        new_message = Message.objects.create(sender=sender, receiver=receiver, content=content)

        # 返回新创建的消息
        return JsonResponse({'message': 'Message sent successfully',
                             'sent_message': {'id': new_message.id, 'sender': new_message.sender.id,
                                              'receiver': new_message.receiver.id, 'content': new_message.content}})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def receive_messages(request, user_id):
    # 从数据库中查询接收者为user_id的所有消息
    received_messages = Message.objects.filter(receiver_id=user_id)

    # 直接构建要返回的数据结构
    messages_list = list(received_messages.values('id', 'sender_id', 'receiver_id', 'content'))
    return JsonResponse(messages_list, safe=False)


def list_messages(request):
    # 从数据库获取所有消息
    messages = Message.objects.all()
    messages_list = [model_to_dict(message, fields=['id', 'sender', 'receiver', 'content']) for message in messages]
    return JsonResponse(messages_list, safe=False)


def search_messages(request, keyword):
    # 根据关键词搜索历史消息
    messages = Message.objects.filter(content__icontains=keyword)
    results_list = [model_to_dict(message, fields=['id', 'sender', 'receiver', 'content']) for message in messages]
    return JsonResponse(results_list, safe=False)




def get_message_detail(request, message_id):
    # 根据消息ID返回特定消息的详情
    message = get_object_or_404(Message, pk=message_id)
    message_detail = model_to_dict(message, fields=['id', 'sender', 'receiver', 'content'])
    return JsonResponse(message_detail)


@require_http_methods(["POST"])
def mark_as_read(request, message_id):
    # 标记消息为已读
    try:
        message = Message.objects.get(id=message_id)
        message.read = True
        message.save()
        return JsonResponse({'message': 'Message marked as read', 'message_id': message_id})
    except Message.DoesNotExist:
        return JsonResponse({'error': 'Message not found'}, status=404)


def mark_as_unread(request, message_id):
    # 标记消息为未读
    try:
        message = Message.objects.get(id=message_id)
        message.read = False
        message.save()
        return JsonResponse({'message': 'Message marked as read', 'message_id': message_id})
    except Message.DoesNotExist:
        return JsonResponse({'error': 'Message not found'}, status=404)


@require_http_methods(["POST"])  # 确保只有POST请求可以调用此视图
def delete_message(request, message_id):
    # 删除消息
    try:
        # 尝试获取指定ID的消息
        message = Message.objects.get(id=message_id)
        # 删除消息
        message.delete()
        return JsonResponse({'message': 'Message deleted successfully', 'message_id': message_id})
    except Message.DoesNotExist:
        # 如果消息不存在，返回错误信息
        return JsonResponse({'error': 'Message not found'}, status=404)


@require_http_methods(["POST"])  # 确保只有POST请求可以调用此视图
def recall_message(request, message_id):
    # 撤回消息
    try:
        # 尝试获取指定ID的消息
        message = Message.objects.get(id=message_id)
        # 删除消息
        message.delete()
        return JsonResponse({'message': 'Message recalled successfully', 'message_id': message_id})
    except Message.DoesNotExist:
        # 如果消息不存在，返回错误信息
        return JsonResponse({'error': 'Message not found'}, status=404)
