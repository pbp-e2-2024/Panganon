from django.shortcuts import render, redirect
from django.contrib import messages
from about_me.models import UserProfile
from authentication.models import User
from django.contrib.auth.hashers import make_password, check_password
import re

def show_main(request):
    if 'user_id' not in request.session:
        return redirect('login_user')
    
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    
    return render(request, "authentication/main.html", {'user': user})

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Username dan password tidak boleh kosong.")
            return redirect('login_user')

        user = User.objects.filter(username=username).first()

        if user is None:
            messages.error(request, "Akun tidak ditemukan. Silakan daftar terlebih dahulu.")
            return redirect('login_user')

        if not check_password(password, user.password):
            messages.error(request, "Password salah.")
            return redirect('login_user')

        request.session['user_id'] = user.id

        return redirect('show_main')
    else:
        return render(request, "authentication/login.html")

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        role = request.POST.get('role')
        image_file = request.FILES.get('image')

        error_messages = []
        
        if not username or not password or not repeat_password or not role:
            error_messages.append("Semua field harus diisi.")

        if len(password) < 8 or not re.search(r"\d", password):
            error_messages.append("Password harus memiliki minimal 8 karakter dan mengandung setidaknya satu angka.")

        if password != repeat_password:
            error_messages.append("Password tidak cocok.")

        if User.objects.filter(username=username).exists():
            error_messages.append("Username sudah digunakan.")

        if image_file:
            if not image_file.content_type in ['image/jpeg', 'image/jpg']:
                error_messages.append("Hanya file JPEG yang diperbolehkan.")
        
        if error_messages:
            for message in error_messages:
                messages.error(request, message)
            return redirect('register')

        hashed_password = make_password(password)

        image_data = image_file.read() if image_file else None

        new_user = User.objects.create(username=username, password=hashed_password, role=role, image=image_data)
        UserProfile.objects.create(user=new_user)
        messages.success(request, "Registrasi berhasil! Silakan login.")
        return redirect('login_user')

    return render(request, "authentication/register.html")

def logout_user(request):
    request.session.flush()  
    messages.success(request, "Anda telah berhasil logout.")
    return redirect('login_user')

from django.http import HttpResponse

def display_image(request, user_id):
    user = User.objects.get(id=user_id)
    if user.image:
        return HttpResponse(user.image, content_type='image/jpeg')
    else:
        return HttpResponse("No image found", status=404)