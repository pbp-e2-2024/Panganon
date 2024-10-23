from django.shortcuts import render, redirect
from django.contrib import messages
from authentication.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout
import re

def show_main(request):
    return render(request, "authentication/main.html")

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

        return redirect('show_main')  # Redirect ke halaman utama setelah sukses
    else:
        return render(request, "authentication/login.html")

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        role = request.POST.get('role')
        image = request.FILES.get('image') if 'image' in request.FILES else None

        error_messages = []
        
        if not username or not password or not repeat_password or not role:
            error_messages.append("Semua field harus diisi.")

        if len(password) < 8 or not re.search(r"\d", password):
            error_messages.append("Password harus memiliki minimal 8 karakter dan mengandung setidaknya satu angka.")

        if password != repeat_password:
            error_messages.append("Password tidak cocok.")

        if User.objects.filter(username=username).exists():
            error_messages.append("Username sudah digunakan.")

        if error_messages:
            for message in error_messages:
                messages.error(request, message)
            return redirect('register')

        hashed_password = make_password(password)
        User.objects.create(username=username, password=hashed_password, role=role, image=image)
        messages.success(request, "Registrasi berhasil! Silakan login.")
        return redirect('login_user')

    return render(request, "authentication/register.html")

def logout_user(request):
    logout(request)  # Ini akan menghapus semua data sesi yang terkait dengan user saat ini
    messages.success(request, "Anda telah berhasil logout.")
    return redirect('login_user')  # Mengarahkan kembali ke halaman login setelah logout