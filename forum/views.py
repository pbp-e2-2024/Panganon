from django.shortcuts import render, redirect, get_object_or_404
from .models import Thread, Post, Comment
from authentication.models import User
from .forms import CommentForm
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST

def forum_home(request):
    if 'user_id' not in request.session:
        return redirect('login_user')
    
    threads = Thread.objects.all()
    return render(request, "forum/home.html", {'threads': threads})

def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    posts = thread.posts.all().prefetch_related('comments')
    
    return render(request, "forum/thread_detail.html", {
        'thread': thread,
        'posts': posts
    })

def create_thread(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.get(id=user_id)
            Thread.objects.create(title=title, created_by=user)
            return redirect('forum_home')
    return render(request, "forum/create_thread.html")

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

@require_POST
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