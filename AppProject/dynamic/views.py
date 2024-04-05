from django.shortcuts import render
"""
包含应用程序的视图函数，处理请求并返回响应，实现应用程序的业务逻辑。
"""
# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# 模拟内容数据，实际情况应该从数据库或其他数据源获取
content_data = [
    {'id': 1, 'title': 'Content 1', 'body': 'This is the body of Content 1'},
    {'id': 2, 'title': 'Content 2', 'body': 'This is the body of Content 2'},
    # 可以根据实际情况添加更多内容信息
]


@csrf_exempt
def publish_content(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')

        # 假设这里是发布内容的逻辑，可以将内容信息保存到数据库中
        new_content = {'id': len(content_data) + 1, 'title': title, 'body': body}
        content_data.append(new_content)

        return JsonResponse({'message': 'Content published successfully', 'content': new_content})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def edit_content(request, content_id):
    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')

        # 假设这里是编辑内容的逻辑，更新对应内容的信息
        for content in content_data:
            if content['id'] == content_id:
                content['title'] = title
                content['body'] = body
                return JsonResponse({'message': 'Content edited successfully', 'content': content})

        return JsonResponse({'error': 'Content not found'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def delete_content(request, content_id):
    if request.method == 'POST':
        for i, content in enumerate(content_data):
            if content['id'] == content_id:
                del content_data[i]
                return JsonResponse({'message': 'Content deleted successfully'})

        return JsonResponse({'error': 'Content not found'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def list_content(request):
    return JsonResponse(content_data)


def get_content_detail(request, content_id):
    for content in content_data:
        if content['id'] == content_id:
            return JsonResponse(content)
    return JsonResponse({'error': 'Content not found'}, status=404)


# 模拟评论数据，实际情况应该从数据库或其他数据源获取
comment_data = [
    {'id': 1, 'user_id': 1, 'content': 'This is a comment'},
    {'id': 2, 'user_id': 2, 'content': 'Another comment'},
    # 可以根据实际情况添加更多评论信息
]


@csrf_exempt
def post_comment(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        content = request.POST.get('content')

        # 假设这里是发表评论的逻辑，可以将评论信息保存到数据库中
        new_comment = {'id': len(comment_data) + 1, 'user_id': user_id, 'content': content}
        comment_data.append(new_comment)

        return JsonResponse({'message': 'Comment posted successfully', 'comment': new_comment})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def get_comment_list(request):
    return JsonResponse(comment_data)


@csrf_exempt
def like_comment(request, comment_id):
    if request.method == 'POST':
        # 假设这里是点赞评论的逻辑
        for comment in comment_data:
            if comment['id'] == comment_id:
                # 假设这里是点赞的处理，可以更新数据库中对应评论的点赞数等信息
                return JsonResponse({'message': 'Comment liked successfully', 'comment': comment})

        return JsonResponse({'error': 'Comment not found'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def follow_user(request, user_id):
    if request.method == 'POST':
        # 假设这里是关注用户的逻辑
        # 可以根据实际情况更新数据库中用户的关注信息
        return JsonResponse({'message': 'User followed successfully', 'user_id': user_id})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def unfollow_user(request, user_id):
    if request.method == 'POST':
        # 假设这里是取关用户的逻辑
        # 可以根据实际情况更新数据库中用户的关注信息
        return JsonResponse({'message': 'User unfollowed successfully', 'user_id': user_id})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

# 模拟用户数据和内容数据，实际情况应该从数据库或其他数据源获取
user_data = [
    {'id': 1, 'name': 'User 1', 'preferences': ['sports', 'music']},
    {'id': 2, 'name': 'User 2', 'preferences': ['technology', 'travel']},
    # 可以根据实际情况添加更多用户信息
]


def search(request):
    keyword = request.GET.get('keyword')
    # 假设这里是关键词搜索的逻辑，可以根据关键词在内容或用户中进行搜索
    # 这里只是简单返回包含关键词的内容和用户信息
    search_results = {
        'content_results': [content for content in content_data if keyword in content['title'] or keyword in content['tags']],
        'user_results': [user for user in user_data if keyword in user['name'] or keyword in user['preferences']]
    }
    return JsonResponse(search_results)

def recommend(request, user_id):
    # 假设这里是根据用户行为和偏好推荐内容的逻辑
    # 可以根据用户的偏好和行为数据生成推荐内容
    recommended_content = [content for content in content_data if any(tag in user_data[user_id-1]['preferences'] for tag in content['tags'])]
    return JsonResponse(recommended_content)