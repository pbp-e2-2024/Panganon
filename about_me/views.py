# Di app profile/views.py

import json
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from about_me.forms import RecipeForm
from .models import Recipe, UserProfile

def profile_view(request, user_id):
    profile = get_object_or_404(UserProfile, user__id=user_id)
    # forum_posts = profile.user.forum_posts.all()
    # ratings = profile.user.ratings.all()

    context = {
        'profile': profile,
        'user': profile.user,  # Menambahkan ini untuk memudahkan akses di template
        # 'posts': forum_posts,
        # 'ratings': ratings
    }
    return render(request, 'about_me/about_me.html', context)

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

@login_required(login_url='login_user')  # Redirect to login page if not authenticated
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user  # Assign the current user to the recipe
            recipe.save()
            return redirect('about_me:profile_detail', user_id=request.user.id)
    else:
        form = RecipeForm()

    return render(request, 'about_me/add_recipe.html', {'form': form})

# View to display full recipe details
def view_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'about_me/recipe_detail.html', {'recipe': recipe})

# View to edit a recipe
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('about_me:view_recipe', recipe_id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'about_me/edit_recipe.html', {'form': form, 'recipe': recipe})