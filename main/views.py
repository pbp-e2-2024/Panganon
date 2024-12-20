from django.shortcuts import render, redirect, reverse
# from main.forms import CatEntryForm
# from main.models import CatEntry

from django.http import HttpResponse
from django.core import serializers

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from django.utils.html import strip_tags


# Create your views here.
# @login_required(login_url='/login')
def show_main(request):
    return render(request, "main.html")

import os
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, HttpResponse
from .forms import SuperuserCreationForm
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def grant_superuser(request):
    correct_secret_key = os.getenv('SECRET_KEY')  
    if request.method == "POST":
        form = SuperuserCreationForm(request.POST)
        if form.is_valid():
            provided_secret_key = form.cleaned_data['secret_key']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            if provided_secret_key == correct_secret_key:
                if User.objects.filter(username=username).exists():
                    user = User.objects.get(username=username)
                    user.is_staff = True
                    user.is_superuser = True
                    user.set_password(password)  
                    user.save()
                    return HttpResponse(f"User '{username}' promoted to superuser.")
                else:
                    User.objects.create_superuser(username, '', password)
                    return HttpResponse(f"Superuser '{username}' created.")
            else:
                return HttpResponseForbidden("Invalid secret key.")
    else:
        form = SuperuserCreationForm()
    
    return render(request, 'grant_superuser.html', {'form': form})