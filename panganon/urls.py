# panganon/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('auth/', include('authentication.urls')),
    path('forum/', include('forum.urls')),
    path('profile/', include('about_me.urls', namespace='about_me')),
    path('daftar_toko/', include('daftar_toko.urls')),
    path('favorites/', include('favorites.urls')),
    path('event/', include('event.urls')),  
    
]