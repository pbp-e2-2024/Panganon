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