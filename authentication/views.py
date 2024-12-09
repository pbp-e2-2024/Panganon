import json
from django.shortcuts import render, redirect # type: ignore
from django.contrib import messages # type: ignore
from about_me.models import UserProfile
from authentication.models import User
from django.contrib.auth.hashers import make_password, check_password # type: ignore
from django.http import JsonResponse # type: ignore
from django.core.exceptions import ObjectDoesNotExist # type: ignore
import re
from django.http import HttpResponse # type: ignore
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore
import base64


def show_main(request):
    if 'user_id' not in request.session:
        return redirect('login_user')

    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    
    return render(request, "main.html", {'user': user})

@csrf_exempt
def login_user(request):
    if 'user_id' in request.session:
        return redirect('show_main')

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

        return redirect('../')
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


def display_image(request, user_id):
    user = User.objects.get(id=user_id)
    if user.image:
        return HttpResponse(user.image, content_type='image/jpeg')
    else:
        return HttpResponse("No image found", status=404)
    
@csrf_exempt
def user_info(request):
    if 'user_id' not in request.session:
        return JsonResponse({'error': 'User not logged in'}, status=401)

    user_id = request.session['user_id']
    try:
        user = User.objects.get(id=user_id)
        user_data = {
            'userID': user.id,
            'username': user.username,
        }
        return JsonResponse(user_data)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

@csrf_exempt
def register_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password1 = data.get('password1')
            password2 = data.get('password2')
            image_base64 = data.get('image')  # Handle image upload if provided
        except json.JSONDecodeError:
            return JsonResponse({
                "status": False,
                "message": "Invalid JSON."
            }, status=400)

        # Check if the passwords match
        if password1 != password2:
            return JsonResponse({
                "status": False,
                "message": "Passwords do not match."
            }, status=400)

        # Check if username is already taken
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "status": False,
                "message": "Username is already taken."
            }, status=400)

        # Hash the password before saving
        hashed_password = make_password(password1)

        # Create the user
        try:
            user = User(
                username=username,
                password=hashed_password 
                  # Save the hashed password
            )
            user.save()

            # Process and save the image if provided
            if image_base64:
                try:
                    img_data = base64.b64decode(image_base64.split(',')[1])  # Decode base64 image
                    user.image = img_data  # Store image as binary data in the model
                    user.save()
                except Exception as e:
                    return JsonResponse({
                        "status": False,
                        "message": f"Failed to process image: {str(e)}"
                    }, status=400)

            # Create UserProfile here (if needed)
            UserProfile.objects.create(user=user)

        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": f"Error creating user: {str(e)}"
            }, status=400)

        # Return user_id in the response
        return JsonResponse({
            "status": True,
            "message": "User successfully registered!",
            "user_id": user.id  # Send back the user_id
        }, status=201)

    return JsonResponse({
        "status": False,
        "message": "Method not allowed."
    }, status=405)

@csrf_exempt
def login_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
        except json.JSONDecodeError:
            return JsonResponse({
                "status": False,
                "message": "Invalid JSON."
            }, status=400)

        # Check if the username exists
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({
                "status": False,
                "message": "Username not found."
            }, status=400)

        # Check if the password matches the hashed password
        if check_password(password, user.password):
            request.session['user_id'] = user.id
            return JsonResponse({
                "username": user.username,
                "status": True,
                "message": "Login successful!"
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Incorrect password."
            }, status=401)

    return JsonResponse({
        "status": False,
        "message": "Method not allowed."
    }, status=405)

@csrf_exempt
def logout_flutter(request):
    username = request.user.username

    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout berhasil!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout gagal."
        }, status=401)