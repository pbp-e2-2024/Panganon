from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Thread, Post, Comment
from authentication.models import User
from .forms import CommentForm

def forum_home(request):
    threads = Thread.objects.all()
    
    if request.headers.get('Accept') == 'application/json':
        threads_data = [
            {
                'id': thread.id,
                'title': thread.title,
                'created_at': thread.created_at.isoformat(),
                'created_by': {
                    'id': thread.created_by.id,
                    'username': thread.created_by.username,
                    'profile_picture': request.build_absolute_uri(
                        reverse('display_image', kwargs={'user_id': thread.created_by.id})
                    ) if thread.created_by.image else None
                }
            }
            for thread in threads
        ]
        return JsonResponse({'threads': threads_data})

    return render(request, "forum/home.html", {'threads': threads})

def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    posts = thread.posts.all().prefetch_related('comments')

    if request.headers.get('Accept') == 'application/json':
        thread_data = {
            'id': thread.id,
            'title': thread.title,
            'created_at': thread.created_at.isoformat(),
            'created_by': {
                'id': thread.created_by.id,
                'username': thread.created_by.username,
                'profile_picture': request.build_absolute_uri(
                    reverse('display_image', kwargs={'user_id': thread.created_by.id})
                ) if thread.created_by.image else None
            },
            'posts': [
                {
                    'id': post.id,
                    'content': post.content,
                    'created_at': post.created_at.isoformat(),
                    'created_by': {
                        'id': post.created_by.id,
                        'username': post.created_by.username,
                        'profile_picture': request.build_absolute_uri(
                            reverse('display_image', kwargs={'user_id': post.created_by.id})
                        ) if post.created_by.image else None
                    },
                    'comments': [
                        {
                            'id': comment.id,
                            'content': comment.content,
                            'created_at': comment.created_at.isoformat(),
                            'created_by': {
                                'id': comment.created_by.id,
                                'username': comment.created_by.username,
                                'profile_picture': request.build_absolute_uri(
                                    reverse('display_image', kwargs={'user_id': comment.created_by.id})
                                ) if comment.created_by.image else None
                            },
                            'parent': comment.parent.id if comment.parent else None
                        }
                        for comment in post.comments.all()
                    ]
                }
                for post in posts
            ]
        }
        return JsonResponse({'thread': thread_data})

    return render(request, "forum/thread_detail.html", {
        'thread': thread,
        'posts': posts
    })

@csrf_exempt
def view_id(request):
    if request.method == 'GET':
        return JsonResponse({'user_id': request.session.get('user_id')})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def create_thread(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.get(id=user_id)
            Thread.objects.create(title=title, created_by=user)
            return redirect('forum_home')
    return render(request, "forum/create_thread.html")

@csrf_exempt
def create_thread_flutter(request):
    if request.method == 'POST':
        title = request.POST['title']
        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.get(id=user_id)
            Thread.objects.create(title=title, created_by=user)
            return JsonResponse({'statusCode': 201}, status=201)
    return JsonResponse({'error': 'User not authenticated'}, status=403)

@csrf_exempt
def delete_thread_flutter(request):
    if request.method == 'POST':
        thread_id = request.POST['thread_id']
        thread = get_object_or_404(Thread, id=thread_id)
        if request.session.get('user_id') != thread.created_by.id:
            return JsonResponse({'statusCode': 403}, status=403)
        
        thread.delete()
        return JsonResponse({'statusCode': 201}, status=201)

@csrf_exempt
def delete_post_flutter(request):
    if request.method == 'POST':
        post_id = request.POST['post_id']
        post = get_object_or_404(Post, id=post_id)
        if request.session.get('user_id') != post.created_by.id:
            return JsonResponse({'statusCode': 403}, status=403)
        post.delete()
        return JsonResponse({'statusCode': 201}, status=201)

@csrf_exempt
def delete_comment_flutter(request):
    if request.method == 'POST':
        comment_id = request.POST['comment_id']
        comment = get_object_or_404(Comment, id=comment_id)
        if request.session.get('user_id') != comment.created_by.id:
            return JsonResponse({'statusCode': 403}, status=403)
        comment.delete()
        return JsonResponse({'statusCode': 201}, status=201)

@csrf_exempt
def add_post_flutter(request, thread_id):
    if request.method == 'POST':
        try:
            content = request.POST['content']
            user_id = request.session.get('user_id')
            if user_id:
                user = User.objects.get(id=user_id)
                thread = get_object_or_404(Thread, id=thread_id)
                post = Post.objects.create(content=content, created_by=user, thread=thread)
                return JsonResponse({'statusCode': 201}, status=201)

            return JsonResponse({'error': 'User not authenticated'}, status=403)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def add_post(request, thread_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.get(id=user_id)
            thread = get_object_or_404(Thread, id=thread_id)
            Post.objects.create(content=content, created_by=user, thread=thread)
            return redirect('thread_detail', thread_id=thread_id)
    return render(request, "forum/add_post.html", {'thread_id': thread_id})

@csrf_exempt
def edit_post_flutter(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        content = request.POST.get('content')

        if not post_id or not content:
            return JsonResponse({'statusCode': 400, 'message': 'Invalid input data'}, status=400)

        post = get_object_or_404(Post, id=post_id)

        user_id = request.session.get('user_id')
        if not user_id or user_id != post.created_by.id:
            return JsonResponse({'statusCode': 403, 'message': 'Permission denied'}, status=403)

        post.content = content
        post.save()

        return JsonResponse({'statusCode': 201, 'message': 'Post updated successfully'}, status=201)

    return JsonResponse({'statusCode': 405, 'message': 'Method not allowed'}, status=405)

@csrf_exempt
def edit_comment_flutter(request):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        content = request.POST.get('content')

        if not comment_id or not content:
            return JsonResponse({'statusCode': 400, 'message': 'Invalid input data'}, status=400)

        comment = get_object_or_404(Comment, id=comment_id)

        user_id = request.session.get('user_id')
        if not user_id or user_id != comment.created_by.id:
            return JsonResponse({'statusCode': 403, 'message': 'Permission denied'}, status=403)

        comment.content = content
        comment.save()

        return JsonResponse({'statusCode': 201, 'message': 'Comment updated successfully'}, status=201)

    return JsonResponse({'statusCode': 405, 'message': 'Method not allowed'}, status=405)

@csrf_exempt
def add_comment_flutter(request):
    if request.method == 'POST':
        try:
            post_id = request.POST.get('post_id')
            parent_id = request.POST.get('parent_id')
            content = request.POST.get('content')

            if not content:
                return JsonResponse({'statusCode': 400, 'message': 'Content is required'}, status=400)
            
            post = get_object_or_404(Post, id=post_id)
            parent_comment = None

            if parent_id:
                parent_comment = get_object_or_404(Comment, id=parent_id)
            
            user_id = request.session.get('user_id')
            if not user_id:
                return JsonResponse({'statusCode': 403, 'message': 'Permission denied'}, status=403)

            user = get_object_or_404(User, id=user_id)
            comment = Comment(
                content=content,
                post=post,
                parent=parent_comment,
                created_by=user
            )
            comment.save()

            return JsonResponse({'statusCode': 201, 'message': 'Comment added successfully'}, status=201)

        except:
            return JsonResponse({'statusCode': 400, 'message': 'Permission denied'}, status=400)

    return JsonResponse({'statusCode': 405, 'message': 'Method not allowed'}, status=405)

@csrf_exempt
def add_comment(request, post_id, parent_id=None):
    post = get_object_or_404(Post, id=post_id)
    parent_comment = None

    if parent_id:
        parent_comment = get_object_or_404(Comment, id=parent_id)

    if 'user_id' not in request.session:
        return redirect('login_user')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.parent = parent_comment

            user_id = request.session.get('user_id')
            if user_id:
                user = User.objects.get(id=user_id)
                comment.created_by = user
                comment.save()
                return redirect('thread_detail', thread_id=post.thread.id)
    else:
        form = CommentForm()
    
    return render(request, "forum/add_comment.html", {
        'form': form,
        'post': post,
        'parent': parent_comment
    })

@require_POST
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.session.get('user_id') != post.created_by.id:
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
    
    post.delete()
    return JsonResponse({'success': True})

@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.session.get('user_id') != comment.created_by.id:
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
    
    comment.delete()
    return JsonResponse({'success': True})

@csrf_exempt
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.session.get('user_id') != post.created_by.id:
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
    
    content = request.POST.get('content')
    if content:
        post.content = content
        post.save()
        return JsonResponse({'success': True, 'content': post.content})
    else:
        return JsonResponse({'success': False, 'error': 'Content cannot be empty'}, status=400)

@csrf_exempt
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.session.get('user_id') != comment.created_by.id:
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'content': comment.content})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid form data'}, status=400)
    
    return render(request, "forum/edit_comment.html", {
        'form': form,
        'comment': comment
    })

def threads_by_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    threads = Thread.objects.filter(created_by=user)
    
    thread_data = {
        request.build_absolute_uri(reverse('thread_detail', args=[thread.id])): thread.title
        for thread in threads
    }
    
    return JsonResponse({'user': user.username, 'threads': thread_data})

@require_POST
def delete_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    if request.session.get('user_id') != thread.created_by.id:
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
    
    thread.delete()
    return JsonResponse({'success': True})