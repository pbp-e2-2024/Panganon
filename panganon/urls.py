# panganon/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('event/', include('event.urls')),  # Ubah ini ke 'event/' tanpa 's'
]
