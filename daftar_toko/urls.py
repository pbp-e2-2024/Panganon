from django.urls import path
from . import views

urlpatterns = [
    path('', views.makanan_list, name='makanan_list'),
]