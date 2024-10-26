from django.urls import path
from authentication.views import login_user, register, show_main, logout_user, user_info
from . import views

urlpatterns = [
    path('', login_user, name='login_user'),
    path('login', login_user, name='login_user'),  # Optional: Jika Anda ingin memiliki path login yang eksplisit
    path('register', register, name='register'),
    path('main', show_main, name='show_main'),  # Tambahkan ini jika belum ada
    path('logout', logout_user, name='logout_user'),
    path('image/<int:user_id>/', views.display_image, name='display_image'),
    path('user_info', user_info, name='user_info'),  
]