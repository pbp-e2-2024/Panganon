# favorites/urls.py
from django.urls import path
from favorites.views import favorites_view, remove_favorite

app_name = 'favorites'

urlpatterns = [
    path('', favorites_view, name='favorites_view'),
    path('remove_favorite/<str:restaurant_id>/', remove_favorite, name='remove_favorite'),
]

