# event/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('<int:pk>/', views.event_detail, name='event_detail'),
    path('create/', views.event_create, name='event_create'),
    path('create-flutter/', views.event_create_flutter, name='event_create_flutter'),
    path('<int:pk>/edit/', views.event_edit, name='event_edit'),
    path('<int:pk>/edit-flutter/', views.event_edit_flutter, name='event_edit_flutter'),
    path('<int:pk>/delete/', views.event_delete, name='event_delete'),
    path('<int:pk>/delete-flutter/', views.event_delete_flutter, name='event_delete_flutter'),
]
