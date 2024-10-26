# Di app profile/urls.py

from django.urls import path
from . import views

app_name = 'about_me'

urlpatterns = [
    path('<int:user_id>/', views.profile_view, name='profile_detail'),
    path('<int:user_id>/edit-bio/', views.edit_bio, name='edit_bio'),
    path('<int:user_id>/edit-preferences/', views.edit_preferences, name='edit_preferences'),
    path('<int:user_id>/get-preferences/', views.get_preferences, name='get_preferences'),
    path('add-recipe/', views.add_recipe, name='add_recipe'),
    path('recipe/<int:recipe_id>/', views.view_recipe, name='view_recipe'),
    path('recipe/edit/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
    path('<int:user_id>/forum-history/', views.all_forum_posts, name='all_forum_posts'),
    path('<int:user_id>/edit-name/', views.edit_name, name='edit_name'),
]