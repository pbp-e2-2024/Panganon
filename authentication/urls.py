from django.urls import path
from authentication.views import logout_flutter, login_user, register, register_flutter, show_main, logout_user, user_info, login_flutter
from . import views

urlpatterns = [
    path('', login_user, name='login_user'),
    path('login_user/', login_user, name='login_user'),  # Optional: Jika Anda ingin memiliki path login yang eksplisit
    path('register/', register, name='register'),
    path('main', show_main, name='show_main'),  # Tambahkan ini jika belum ada
    path('logout', logout_user, name='logout_user'),
    path('image/<int:user_id>/', views.display_image, name='display_image'),
    path('user_info/', views.user_info, name='user_info'),  
    path('login_flutter/', login_flutter, name='login'),
    path('register_flutter/', register_flutter, name='register_flutter'),
    path('logout_flutter/', logout_flutter, name='logout_flutter'),
]