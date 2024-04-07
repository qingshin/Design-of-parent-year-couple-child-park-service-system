from django.shortcuts import render

"""
包含应用程序的视图函数，处理请求并返回响应，实现应用程序的业务逻辑。
"""
# Create your views here.
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseForbidden
from django import forms
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Post, Media, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['media_type', 'file_path']
        widgets = {'media_type': forms.HiddenInput()}


@login_required
@require_http_methods(["POST"])
def publish_content(request):
    """
    这个函数将接收来自前端的数据（可能包括文本内容和一个或多个媒体文件），然后创建一个新的Post实例以及相应的Media实例（如果有媒体文件的话）。
    以下是一个简单的示例，展示了如何在Django视图中实现这个功能。这个示例假设你使用Django的表单来提交数据，且媒体文件通过多文件上传的方式提交
    用户验证：使用@login_required装饰器确保只有登录的用户可以发布动态。
    请求方法限制：使用@require_http_methods(["POST"])装饰器确保只处理POST请求。
    获取文本内容：从POST请求中获取文本内容。如果没有提供内容，则默认为空字符串。
    创建Post实例：使用请求中的文本内容和当前登录的用户信息创建一个新的Post实例。
    处理媒体文件：从请求中获取名为media_files的文件列表。对于每个文件，根据其MIME类型判断是图片还是视频，并为每个文件创建一个Media实例，关联到刚创建的Post实例。
    响应：返回一个JSON响应，包含操作成功的消息和新创建的Post的ID。
    """
    # 获取文本内容
    content = request.POST.get('content', '')

    # 创建Post实例
    post = Post.objects.create(user=request.user, content=content)

    # 处理媒体文件
    media_files = request.FILES.getlist('media_files')  # 假设前端字段名为'media_files'
    for file in media_files:
        # 简单示例，实际应用中可能需要根据文件类型进行更复杂的处理
        media_type = 'image' if file.content_type.startswith('image/') else 'video'
        Media.objects.create(post=post, media_type=media_type, file_path=file)

    return JsonResponse({'message': 'Content published successfully.', 'post_id': post.id})


@login_required
@require_http_methods(["POST"])
def edit_content(request, content_id):  # 修改参数名为content_id以匹配URL模式
    # 尝试获取要编辑的Post实例
    try:
        post = Post.objects.get(id=content_id, user=request.user)
    except Post.DoesNotExist:
        return JsonResponse({'message': 'Post not found or access denied.'}, status=404)

    # 获取更新的内容
    content = request.POST.get('content', '')
    if content:
        post.content = content
        post.save()
        return JsonResponse({'message': 'Content updated successfully.'})
    else:
        return JsonResponse({'message': 'No content provided.'}, status=400)


@login_required
@require_http_methods(["DELETE"])
def delete_content(request, content_id):
    try:
        post = Post.objects.get(id=content_id)
    except Post.DoesNotExist:
        return HttpResponseNotFound({'message': 'Post not found.'})

    # 检查当前登录用户是否为动态的发布者
    if post.user != request.user:
        return HttpResponseForbidden({'message': 'You do not have permission to delete this post.'})

    post.delete()
    return JsonResponse({'message': 'Post deleted successfully.'})


def list_content(request):
    posts_list = Post.objects.all().order_by('-created_at')  # 获取所有动态并按创建时间降序排序
    page = request.GET.get('page', 1)  # 从请求的查询参数中获取页码
    paginator = Paginator(posts_list, 10)  # 每页显示10条动态

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # 如果页码不是整数，展示第一页
        posts = paginator.page(1)
    except EmptyPage:
        # 如果页码超出范围，展示最后一页
        posts = paginator.page(paginator.num_pages)

    # 将动态数据及其关联的媒体文件序列化为JSON格式
    posts_data = []
    for post in posts:
        media_files = Media.objects.filter(post=post).values('media_type', 'file_path')
        post_data = {
            'id': post.id,
            'user': post.user.username,
            'content': post.content,
            'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'media': list(media_files)
        }
        posts_data.append(post_data)

    return JsonResponse({'posts': posts_data, 'page': int(page), 'pages': paginator.num_pages}, safe=False)


def get_content_detail(request, content_id):
    try:
        # 尝试获取指定ID的动态
        post = Post.objects.get(id=content_id)
    except Post.DoesNotExist:
        # 如果动态不存在，返回404错误
        return HttpResponseNotFound({'message': 'Post not found.'})

    # 获取与动态相关联的媒体文件信息
    media_files = Media.objects.filter(post=post).values('media_type', 'file_path')

    # 构建动态的详细信息
    post_detail = {
        'id': post.id,
        'user': post.user.username,
        'content': post.content,
        'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'media': list(media_files)
    }

    # 如果有其他需要包含的信息，比如评论、点赞数等，也可以在这里添加

    return JsonResponse(post_detail)


@login_required
@require_http_methods(["POST"])
@csrf_exempt
def publish_comment(request, post_id):
    # 确保动态存在
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'message': 'Post not found.'}, status=404)

    # 获取评论内容
    content = request.POST.get('content', '').strip()
    if not content:
        return JsonResponse({'message': 'Comment content cannot be empty.'}, status=400)

    # 创建评论实例
    comment = Comment.objects.create(content=content, post=post, user=request.user)

    return JsonResponse({'message': 'Comment published successfully.', 'comment_id': comment.id})

#
# @csrf_exempt
# def like_comment(request, comment_id):
#     if request.method == 'POST':
#         # 假设这里是点赞评论的逻辑
#         for comment in comment_data:
#             if comment['id'] == comment_id:
#                 # 假设这里是点赞的处理，可以更新数据库中对应评论的点赞数等信息
#                 return JsonResponse({'message': 'Comment liked successfully', 'comment': comment})
#
#         return JsonResponse({'error': 'Comment not found'}, status=404)
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405)
#
#
# @csrf_exempt
# def follow_user(request, user_id):
#     if request.method == 'POST':
#         # 假设这里是关注用户的逻辑
#         # 可以根据实际情况更新数据库中用户的关注信息
#         return JsonResponse({'message': 'User followed successfully', 'user_id': user_id})
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405)
#
#
# @csrf_exempt
# def unfollow_user(request, user_id):
#     if request.method == 'POST':
#         # 假设这里是取关用户的逻辑
#         # 可以根据实际情况更新数据库中用户的关注信息
#         return JsonResponse({'message': 'User unfollowed successfully', 'user_id': user_id})
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405)
#
# # 模拟用户数据和内容数据，实际情况应该从数据库或其他数据源获取
# user_data = [
#     {'id': 1, 'name': 'User 1', 'preferences': ['sports', 'music']},
#     {'id': 2, 'name': 'User 2', 'preferences': ['technology', 'travel']},
#     # 可以根据实际情况添加更多用户信息
# ]
#
#
# def search(request):
#     keyword = request.GET.get('keyword')
#     # 假设这里是关键词搜索的逻辑，可以根据关键词在内容或用户中进行搜索
#     # 这里只是简单返回包含关键词的内容和用户信息
#     search_results = {
#         'content_results': [content for content in content_data if keyword in content['title'] or keyword in content['tags']],
#         'user_results': [user for user in user_data if keyword in user['name'] or keyword in user['preferences']]
#     }
#     return JsonResponse(search_results)
#
# def recommend(request, user_id):
#     # 假设这里是根据用户行为和偏好推荐内容的逻辑
#     # 可以根据用户的偏好和行为数据生成推荐内容
#     recommended_content = [content for content in content_data if any(tag in user_data[user_id-1]['preferences'] for tag in content['tags'])]
#     return JsonResponse(recommended_content)
