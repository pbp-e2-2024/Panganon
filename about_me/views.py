import json
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from forum.models import Post
from .models import UserProfile
from django.core.paginator import Paginator

def profile_view(request, user_id):
    profile = get_object_or_404(UserProfile, user__id=user_id)
    is_own_profile = (request.session.get('user_id') == user_id)
    forum_posts = Post.objects.filter(created_by=profile.user).order_by('-created_at')[:3]

    context = {
        'profile': profile,
        'user': profile.user,
        'forum_posts': forum_posts,
        'is_own_profile': is_own_profile,
    }
    return render(request, 'about_me/about_me.html', context)

def edit_name(request, user_id):
    if request.method == 'POST':
        profile = get_object_or_404(UserProfile, user__id=user_id)
        data = json.loads(request.body)
        new_name = data.get('name', '').strip()

        # Simpan nama baru jika tidak kosong
        if new_name:
            profile.user.name = new_name
            profile.user.save()

        return JsonResponse({'name': new_name})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def edit_bio(request, user_id):
    profile = get_object_or_404(UserProfile, user__id=user_id)

    if request.method == 'POST':
        bio = request.POST.get('bio')
        profile.bio = bio
        profile.save()
        return redirect('profile_detail', user_id=user_id)

    return render(request, 'about_me/edit_bio.html', {'profile': profile})

def edit_preferences(request, user_id):
    profile = get_object_or_404(UserProfile, user__id=user_id)

    if request.method == 'POST':
        preferences = request.POST.get('preferences')
        profile.food_preferences = preferences
        profile.save()
        return redirect('profile_detail', user_id=user_id)

    return render(request, 'about_me/edit_preferences.html', {'profile': profile})

# View untuk mendapatkan preferensi yang sudah dipilih
def get_preferences(request, user_id):
    profile = get_object_or_404(UserProfile, user__id=user_id)
    preferences = profile.food_preferences.split(", ") if profile.food_preferences else []
    return JsonResponse({'preferences': preferences})

# View untuk menyimpan preferensi melalui AJAX
def edit_preferences(request, user_id):
    if request.method == 'POST':
        profile = get_object_or_404(UserProfile, user__id=user_id)
        data = json.loads(request.body)
        selected_preferences = data.get('preferences', [])

        # Simpan preferensi yang dipilih
        profile.food_preferences = ", ".join(selected_preferences)
        profile.save()

        return JsonResponse({'preferences': selected_preferences})
    return JsonResponse({'error': 'Invalid request'}, status=400)
    
def edit_bio(request, user_id):
    if request.method == 'POST':
        profile = get_object_or_404(UserProfile, user__id=user_id)
        data = json.loads(request.body)
        new_bio = data.get('bio', '').strip()  # Menghapus spasi di depan dan belakang

        # Simpan bio baru, jika kosong set sebagai string kosong
        profile.bio = new_bio if new_bio != "" else ""
        profile.save()

        return JsonResponse({'bio': new_bio})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def all_forum_posts(request, user_id):
    profile = get_object_or_404(UserProfile, user__id=user_id)
    forum_posts = Post.objects.filter(created_by=profile.user).order_by('-created_at')
    
    # Pagination jika diperlukan, misalnya menampilkan 10 post per halaman
    paginator = Paginator(forum_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'profile': profile,
        'forum_posts': page_obj,
    }
    return render(request, 'about_me/all_forum_posts.html', context)
