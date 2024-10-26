# Di app profile/views.py

import json
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from about_me.forms import RecipeForm
from forum.models import Post
from .models import Recipe, UserProfile
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


from django.shortcuts import render, redirect
from .forms import RecipeForm
from .models import User, Recipe

def add_recipe(request):
    if 'user_id' not in request.session:
        return redirect('login_user')

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)

        user_id = request.session.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return redirect('login_user')  

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = user
            recipe.save()
            return redirect('about_me:profile_detail', user_id=user.id)
        else:
            print("Form is not valid:", form.errors)
    else:
        form = RecipeForm()

    return render(request, 'about_me/add_recipe.html', {'form': form})

# View to display full recipe details
def view_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    is_own_recipe = recipe.user == request.user  # Memeriksa apakah pengguna sedang melihat resep milik mereka sendiri
    return render(request, 'about_me/recipe_detail.html', {'recipe': recipe, 'is_own_recipe': is_own_recipe})

# View to edit a recipe
def edit_recipe(request, recipe_id):
    
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if recipe.user != request.user:
        return redirect('about_me:profile_detail', user_id=request.user.id)  # Mengarahkan kembali jika pengguna mencoba mengedit resep yang bukan milik mereka

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('about_me:view_recipe', recipe_id=recipe.id)  # Kembali ke halaman detail resep setelah disimpan
    else:
        form = RecipeForm(instance=recipe)  # Mengisi form dengan data yang ada

    return render(request, 'about_me/edit_recipe.html', {'form': form, 'recipe': recipe})

from django.http import JsonResponse
from .models import Recipe, UserProfile

def user_recipes_json(request, user_id):
    profile = get_object_or_404(UserProfile, user__id=user_id)
    recipes = Recipe.objects.filter(user=profile.user)
    
    recipes_data = [
        {
            'id': recipe.id,
            'name': recipe.name, 
            'description': recipe.description,
            'ingredients': recipe.ingredients,
            'steps': recipe.steps,
            'image': recipe.image.url if recipe.image else None,
            'created_at': str(recipe.created_at),  
        }
        for recipe in recipes
    ]
    
    return JsonResponse({'recipes': recipes_data})
