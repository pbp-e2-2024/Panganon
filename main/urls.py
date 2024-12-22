from django.urls import path
from main.views import show_main, grant_superuser

app_name = 'main'
urlpatterns = [
    path('', show_main, name='show_home'),
    path('create-admin/', grant_superuser, name='grant_superuser'),
]