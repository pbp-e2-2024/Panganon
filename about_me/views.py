import json  # Untuk mengolah data JSON
from django.http import JsonResponse  # Untuk merespons dalam format JSON
from django.shortcuts import redirect, render, get_object_or_404  # Shortcut untuk redirect, render template, dan handling 404
from django.contrib.auth.decorators import login_required  # Dekorator untuk membatasi akses hanya untuk user login
from forum.models import Post, Thread # Model postingan dari forum
from .models import UserProfile  # Model profil pengguna
from django.core.paginator import Paginator  # Untuk membagi data ke dalam beberapa halaman

def profile_view(request, user_id):  # Menampilkan profil pengguna
    profile = get_object_or_404(UserProfile, user__id=user_id)  # Dapatkan profil berdasarkan user_id
    is_own_profile = (request.session.get('user_id') == user_id)  # Cek apakah profil milik user yang login
    forum_posts = Post.objects.filter(created_by=profile.user).order_by('-created_at')[:3]  # Ambil 3 postingan terbaru
    context = {'profile': profile, 'user': profile.user, 'forum_posts': forum_posts, 'is_own_profile': is_own_profile}
    return render(request, 'about_me/about_me.html', context)  # Render halaman profil

def edit_name(request, user_id):  # Mengedit nama user
    if request.method == 'POST':
        profile = get_object_or_404(UserProfile, user__id=user_id)  # Dapatkan profil berdasarkan user_id
        data = json.loads(request.body)  # Parse JSON dari body request
        new_name = data.get('name', '').strip()  # Ambil nama baru dan hilangkan spasi ekstra
        if new_name:
            profile.user.name = new_name  # Simpan nama baru jika tidak kosong
            profile.user.save()
        return JsonResponse({'name': new_name})  # Kirim JSON respons nama baru atau error jika bukan POST

def edit_bio(request, user_id):  # Mengedit bio pengguna
    profile = get_object_or_404(UserProfile, user__id=user_id)
    if request.method == 'POST':
        bio = request.POST.get('bio')
        profile.bio = bio  # Set bio baru
        profile.save()
        return redirect('profile_detail', user_id=user_id)  # Redirect ke profil
    return render(request, 'about_me/edit_bio.html', {'profile': profile})  # Render halaman edit_bio

def edit_preferences(request, user_id):  # Mengedit preferensi makanan
    profile = get_object_or_404(UserProfile, user__id=user_id)
    if request.method == 'POST':
        preferences = request.POST.get('preferences')  # Ambil preferensi baru
        profile.food_preferences = preferences  # Simpan preferensi
        profile.save()
        return redirect('profile_detail', user_id=user_id)
    return render(request, 'about_me/edit_preferences.html', {'profile': profile})  # Render halaman edit_preferences

def get_preferences(request, user_id):  # Mengambil preferensi yang disimpan
    profile = get_object_or_404(UserProfile, user__id=user_id)
    preferences = profile.food_preferences.split(", ") if profile.food_preferences else []  # Ambil preferensi dalam list
    return JsonResponse({'preferences': preferences})  # Kirim JSON preferensi

def edit_preferences(request, user_id):  # Mengedit preferensi menggunakan AJAX
    if request.method == 'POST':
        profile = get_object_or_404(UserProfile, user__id=user_id)
        data = json.loads(request.body)
        selected_preferences = data.get('preferences', [])
        profile.food_preferences = ", ".join(selected_preferences)  # Simpan preferensi yang dipilih
        profile.save()
        return JsonResponse({'preferences': selected_preferences})  # Kirim JSON respons preferensi baru

def edit_bio(request, user_id):  # Mengedit bio menggunakan AJAX
    if request.method == 'POST':
        profile = get_object_or_404(UserProfile, user__id=user_id)
        data = json.loads(request.body)
        new_bio = data.get('bio', '').strip()
        profile.bio = new_bio if new_bio else ""  # Simpan bio baru atau kosongkan jika kosong
        profile.save()
        return JsonResponse({'bio': new_bio})  # Kirim JSON bio baru

def all_forum_posts(request, user_id):  # Menampilkan semua postingan forum user
    profile = get_object_or_404(UserProfile, user__id=user_id)
    forum_posts = Post.objects.filter(created_by=profile.user).order_by('-created_at')  # Ambil semua postingan forum
    paginator = Paginator(forum_posts, 10)  # Buat pagination dengan 10 postingan per halaman
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'profile': profile, 'forum_posts': page_obj}
    return render(request, 'about_me/all_forum_posts.html', context)  # Render halaman all_forum_posts


def show_json_all(request):
    # Ambil semua user profile dari database
    user_profiles = UserProfile.objects.all()

    # Membuat list untuk menampung data pengguna
    profiles_data = []

    for profile in user_profiles:
        # Ambil postingan forum user
        forum_posts = Post.objects.filter(created_by=profile.user).order_by('-created_at')
        forum_posts_data = []

        # Loop untuk menyusun data forum posts
        for post in forum_posts:
            thread = post.thread  # Ambil thread terkait dengan post
            forum_posts_data.append({
                'post_id': post.id,
                'thread_title': thread.title,  # Menyertakan title dari Thread
                'content': post.content,  # Menyertakan content dari Post
                'created_at': post.created_at,
                'updated_at': post.created_at  # Atau post.updated_at jika ada
            })

        # Tambahkan data profil dan forum posts ke dalam profiles_data
        profiles_data.append({
            'userID': profile.user.id,
            'username': profile.user.username,
            'bio': profile.bio,
            'food_preferences': profile.food_preferences.split(', ') if profile.food_preferences else [],
            'forum_posts': forum_posts_data  # Menambahkan data forum posts
        })

    # Mengembalikan data dalam format JSON
    return JsonResponse(profiles_data, safe=False)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def edit_name_flutter(request, user_id):
    if request.method == 'POST':
        profile = get_object_or_404(UserProfile, user__id=user_id)
        data = json.loads(request.body)
        new_name = data.get('name', '').strip()
        if not new_name:
            return JsonResponse({'error': 'Name cannot be empty'}, status=400)
        profile.user.name = new_name
        profile.user.save()
        return JsonResponse({'name': new_name})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def edit_bio_flutter(request, user_id):
    if request.method == 'POST':
        profile = get_object_or_404(UserProfile, user__id=user_id)
        data = json.loads(request.body)
        new_bio = data.get('bio', '').strip()
        if not new_bio:
            return JsonResponse({'error': 'Bio cannot be empty'}, status=400)
        profile.bio = new_bio
        profile.save()
        return JsonResponse({'bio': new_bio})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def edit_preferences_flutter(request, user_id):
    if request.method == 'POST':
        profile = get_object_or_404(UserProfile, user__id=user_id)
        data = json.loads(request.body)
        new_preferences = data.get('preferences', [])
        if not isinstance(new_preferences, list):
            return JsonResponse({'error': 'Preferences should be a list'}, status=400)
        profile.food_preferences = ', '.join(new_preferences)  # Mengubah list menjadi string
        profile.save()
        return JsonResponse({'preferences': profile.food_preferences})  # Mengirim kembali string
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def get_preferences_flutter(request, user_id):
    if request.method == 'GET':
        profile = get_object_or_404(UserProfile, user__id=user_id)
        preferences = profile.food_preferences  # Mengambil preferensi dari profile

        return JsonResponse({'preferences': preferences})

    return JsonResponse({'error': 'Invalid request method'}, status=400)