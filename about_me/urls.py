# Di app profile/urls.py

from django.urls import path
from . import views

app_name = 'about_me'

urlpatterns = [
    path('<int:user_id>/', views.profile_view, name='profile_detail'),
    path('<int:user_id>/edit-bio/', views.edit_bio, name='edit_bio'),
    path('<int:user_id>/edit-preferences/', views.edit_preferences, name='edit_preferences'),
    path('<int:user_id>/get-preferences/', views.get_preferences, name='get_preferences'),
]