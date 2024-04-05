from django.shortcuts import render

"""
包含应用程序的视图函数，处理请求并返回响应，实现应用程序的业务逻辑。
"""
# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def get_activity_list(request):
    # 假设这里是从数据库或其他数据源获取活动列表的逻辑
    activity_list = [
        {'id': 1, 'name': 'Activity 1', 'date': '2024-03-20'},
        {'id': 2, 'name': 'Activity 2', 'date': '2024-03-25'},
        # 可以根据实际情况添加更多活动信息
    ]

    return JsonResponse(activity_list, safe=False)


def get_activity_detail(request, activity_id):
    # 假设这里是从数据库或其他数据源获取特定活动详情的逻辑
    activity = {
        'id': activity_id,
        'name': 'Activity ' + str(activity_id),
        'date': '2024-03-20',
        'description': 'This is the description of Activity ' + str(activity_id)
        # 可以根据实际情况添加更多活动详情字段
    }

    return JsonResponse(activity)


@csrf_exempt
def create_reservation(request):
    """
    用于处理创建预约的请求的视图函数。接收POST请求，从请求中获取预约信息，如活动ID、用户ID、预约时间等，然后可以将预约信息保存到数据库中。
    最后返回一个包含预约成功消息的JSON响应。

    :param request: 包含预约信息的请求对象
    :return: 返回JSON响应，包含预约成功或失败的消息
    """
    if request.method == 'POST':
        # 假设从请求中获取预约信息，如活动ID、用户ID、预约时间等
        activity_id = request.POST.get('activity_id')
        user_id = request.POST.get('user_id')
        reservation_time = request.POST.get('reservation_time')

        # 假设这里是创建预约的逻辑，可以将预约信息保存到数据库中
        # 这里只是简单返回预约成功的消息，实际情况根据需求进行处理
        return JsonResponse({'message': 'Reservation created successfully'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def get_reservation_detail(request, reservation_id):
    """
    用于处理获取特定预约详情的请求的视图函数。接收预约ID作为参数，从数据库或其他数据源获取对应预约的详细信息，并返回包含预约详情的JSON响应。

    :param request: 包含获取预约详情的请求对象
    :param reservation_id: 要获取详情的预约ID
    :return: 返回JSON响应，包含特定预约的详细信息
    """
    # 假设这里是从数据库或其他数据源获取特定预约详情的逻辑
    reservation = {
        'id': reservation_id,
        'activity_id': 1,
        'user_id': 1,
        'reservation_time': '2024-03-20 10:00:00',
        'status': 'Confirmed'
        # 可以根据实际情况添加更多预约详情字段
    }

    return JsonResponse(reservation)


def cancel_reservation(request, reservation_id):
    """
    用于处理取消预约的请求的视图函数。它接收POST请求，从请求中获取预约ID，然后可以执行取消预约的逻辑，如从数据库中标记预约为取消状态。最后返回一个包含取消预约成功消息的JSON响应。
    :param request:
    :param reservation_id:
    :return:
    """
    if request.method == 'POST':
        # 假设这里是取消预约的逻辑，可以从数据库中标记预约为取消状态
        # 这里只是简单返回取消预约成功的消息，实际情况根据需求进行处理
        return JsonResponse({'message': 'Reservation canceled successfully'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


from django.http import JsonResponse


def create_activity(request):
    """
    用于处理管理员创建活动的请求的视图函数。它接收POST请求，从请求中获取活动信息，如活动名称、日期、地点等，然后可以将活动信息保存到数据库中。最后返回一个包含活动创建成功消息的JSON响应。
    :param request:
    :return:
    """
    if request.method == 'POST':
        # 假设这里是从请求中获取活动信息，如活动名称、日期、地点等
        name = request.POST.get('name')
        date = request.POST.get('date')
        location = request.POST.get('location')

        # 假设这里是创建活动的逻辑，可以将活动信息保存到数据库中
        # 这里只是简单返回活动创建成功的消息，实际情况根据需求进行处理
        return JsonResponse({'message': 'Activity created successfully'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def edit_activity(request, activity_id):
    """
    用于处理编辑活动的请求的视图函数。它接收POST请求，从请求中获取编辑后的活动信息，如活动名称、日期、地点等，然后可以更新数据库中对应活动的信息。最后返回一个包含活动编辑成功消息的JSON响应。
    :param request:
    :param activity_id:
    :return:
    """
    if request.method == 'POST':
        # 假设这里是从请求中获取编辑后的活动信息，如活动名称、日期、地点等
        name = request.POST.get('name')
        date = request.POST.get('date')
        location = request.POST.get('location')

        # 假设这里是编辑活动的逻辑，可以更新数据库中对应活动的信息
        # 这里只是简单返回活动编辑成功的消息，实际情况根据需求进行处理
        return JsonResponse({'message': 'Activity edited successfully'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def delete_activity(request, activity_id):
    """
    用于处理删除活动的请求的视图函数。它接收POST请求，从请求中获取要删除的活动ID，然后可以从数据库中删除对应的活动。最后返回一个包含活动删除成功消息的JSON响应。
    :param request:
    :param activity_id:
    :return:
    """
    if request.method == 'POST':
        # 假设这里是删除活动的逻辑，可以从数据库中删除对应活动
        # 这里只是简单返回活动删除成功的消息，实际情况根据需求进行处理
        return JsonResponse({'message': 'Activity deleted successfully'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def manage_reservation(request, reservation_id):
    """
    用于处理管理预约的请求的视图函数。它接收POST请求，从请求中获取要管理的预约ID，然后可以对预约进行确认、取消等操作。最后返回一个包含预约管理成功消息的JSON响应。
    :param request:
    :param reservation_id:
    :return:
    """
    if request.method == 'POST':
        # 假设这里是管理预约的逻辑，可以对预约进行确认、取消等操作
        # 这里只是简单返回预约管理成功的消息，实际情况根据需求进行处理
        return JsonResponse({'message': 'Reservation managed successfully'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)