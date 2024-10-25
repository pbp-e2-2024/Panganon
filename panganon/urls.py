# panganon/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('forum/', include('forum.urls')),
    path('event/', include('event.urls')),  

]
