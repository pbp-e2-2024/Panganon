# Di app profile/urls.py

from django.urls import path
from . import views

app_name = 'about_me'

urlpatterns = [
    path('<int:user_id>/', views.profile_view, name='profile_detail'),
    path('<int:user_id>/edit-bio/', views.edit_bio, name='edit_bio'),
    path('<int:user_id>/edit-preferences/', views.edit_preferences, name='edit_preferences'),
    path('<int:user_id>/get-preferences/', views.get_preferences, name='get_preferences'),
    path('<int:user_id>/forum-history/', views.all_forum_posts, name='all_forum_posts'),
    path('<int:user_id>/edit-name/', views.edit_name, name='edit_name'),
    path('show_json_all/', views.show_json_all, name='show_json_all'),
    path('edit_name/<int:user_id>/', views.edit_name_flutter, name='edit_name_flutter'),  # Edit nama pengguna
    path('edit_bio/<int:user_id>/', views.edit_bio_flutter, name='edit_bio_flutter'),  # Edit bio pengguna
    path('edit_preferences/<int:user_id>/', views.edit_preferences_flutter, name='edit_preferences_flutter'),  # Edit preferensi pengguna
    path('get_preferences/<int:user_id>/', views.get_preferences_flutter, name='get_preferences_flutter'),
]