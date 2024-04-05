from django.shortcuts import render

"""
包含应用程序的视图函数，处理请求并返回响应，实现应用程序的业务逻辑。
"""
# Create your views here.
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import logout


@csrf_exempt
@require_POST
def user_login(request):
    """
    用于处理用户登录请求的视图函数。接收POST请求，验证用户身份，生成并返回访问令牌。

    :param request: 包含用户登录信息的请求对象
    :return: 返回JSON响应，包含登录成功或失败的消息
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'})
        else:
            return JsonResponse({'message': 'Login failed'}, status=400)


def login_test_page(request):
    return render(request, 'authAPP/LoginTestPage.html')


@csrf_exempt
@require_POST
def user_register(request):
    """
    用于处理用户注册请求的视图函数。接收POST请求，从请求中获取用户名、电子邮件和密码，并使用Django提供的用户模型创建新用户。
    如果用户名已存在或请求缺少必要信息，会返回相应的错误消息。最后，如果注册成功，会返回注册成功的消息。

    :param request: 包含用户注册信息的请求对象
    :return: 返回JSON响应，包含注册成功或失败的消息
    """
    User = get_user_model()
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')

    if not username or not email or not password:
        return JsonResponse({'error': 'Please provide username, email, and password'}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already exists'}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)

    return JsonResponse({'message': 'User registered successfully'})


def register_test_page(request):
    return render(request, 'authAPP/RegisterTestPage.html')


@csrf_exempt
@require_POST
def user_logout(request):
    """
    用于处理用户登出请求的视图函数。接收POST请求，调用Django提供的logout函数来登出当前用户，并返回登出成功的消息。

    :param request: 包含用户登出信息的请求对象
    :return: 返回JSON响应，包含登出成功的消息
    """
    logout(request)
    return JsonResponse({'message': 'User logged out successfully'})


@csrf_exempt
@require_POST
def get_user_info(request, user_id):
    """
    用于处理获取用户信息请求的视图函数。接收用户ID作为参数，从数据库中获取对应用户的信息，并返回用户的基本信息，如用户名、电子邮件、是否为管理员等。

    :param request: 包含获取用户信息的请求对象
    :param user_id: 要获取信息的用户ID
    :return: 返回JSON响应，包含用户的基本信息
    """
    User = get_user_model()
    try:
        user = User.objects.get(id=user_id)
        user_info = {
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff,
            'is_active': user.is_active
            # 可以根据需要添加其他用户信息字段
        }
        return JsonResponse(user_info)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)


@csrf_exempt
@require_POST
def get_following_users(request, user_id):
    """
    用于处理获取关注的用户列表请求的视图函数。接收用户ID作为参数，从数据库中获取对应用户关注的用户列表，并返回关注用户的基本信息，如用户名和电子邮件。

    :param request: 包含获取关注用户列表的请求对象
    :param user_id: 要获取关注用户列表的用户ID
    :return: 返回JSON响应，包含关注用户的基本信息列表
    """
    User = get_user_model()
    try:
        user = User.objects.get(id=user_id)
        following_users = user.following.all()
        following_list = [{'username': following_user.username, 'email': following_user.email} for following_user in
                          following_users]
        return JsonResponse(following_list, safe=False)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)


@csrf_exempt
@require_POST
def get_followers(request, user_id):
    """
    用于处理获取粉丝列表请求的视图函数。接收用户ID作为参数，从数据库中获取对应用户的粉丝列表，并返回粉丝的基本信息，如用户名和电子邮件。

    :param request: 包含获取粉丝列表的请求对象
    :param user_id: 要获取粉丝列表的用户ID
    :return: 返回JSON响应，包含粉丝的基本信息列表
    """
    User = get_user_model()
    try:
        user = User.objects.get(id=user_id)
        followers = user.followers.all()
        followers_list = [{'username': follower.username, 'email': follower.email} for follower in followers]
        return JsonResponse(followers_list, safe=False)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
