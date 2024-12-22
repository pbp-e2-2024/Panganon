# event/views.py
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from authentication.models import User  # Impor User dari modul authentication
from .models import Event
from .forms import EventForm
from .serializers import EventSerializer

def event_list(request):
    event = Event.objects.select_related('created_by').all()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        event_data = EventSerializer(event, many=True)
        return JsonResponse(event_data.data, safe=False)
    return render(request, 'event/event_list.html', {'event': event})

def event_detail(request, pk):
    # Mendapatkan detail event berdasarkan primary key (pk)
    event = get_object_or_404(Event, pk=pk)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        event_data = EventSerializer(event)
        return JsonResponse(event_data.data, safe=False)
    return render(request, 'event/event_detail.html', {'event': event})

def event_create(request):
    # Cek jika user sudah login
    if 'user_id' not in request.session:
        messages.error(request, "Anda harus login terlebih dahulu.")
        return redirect('login_user')

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)

            try:
                user_id = request.session.get('user_id')  # Ambil user ID dari session
                user = User.objects.get(id=user_id)  # Ambil user dari model `authentication.models.User`
                event.created_by = user
            except User.DoesNotExist:
                return JsonResponse({'success': False, 'errors': 'User tidak ditemukan.'})

            event.save()
            return JsonResponse({'success': True, 'event_id': event.pk})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = EventForm()
    return render(request, 'event/event_form.html', {'form': form, 'form_title': 'Create', 'form_button_text': 'Create'})

def event_edit(request, pk):
    if 'user_id' not in request.session:
        messages.error(request, "Anda harus login terlebih dahulu.")
        return redirect('login_user')

    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'event_id': event.pk})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = EventForm(instance=event)
    return render(request, 'event/event_form.html', {'form': form, 'form_title': 'Edit', 'form_button_text': 'Update'})

def event_delete(request, pk):
    if 'user_id' not in request.session:
        messages.error(request, "Anda harus login terlebih dahulu.")
        return redirect('login_user')

    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    
    return render(request, 'event/event_delete_confirmation.html', {'event': event})


@csrf_exempt
def event_create_flutter(request):
    # Cek jika user sudah login
    if 'user_id' not in request.session:
        messages.error(request, "Anda harus login terlebih dahulu.")
        return JsonResponse({'success': False, 'errors': 'Unauthenticated'})

    if request.method == 'POST':
        body = json.loads(request.body)
        form = EventForm(body)
        if form.is_valid():
            event = form.save(commit=False)
            try:
                user_id = request.session.get('user_id')  # Ambil user ID dari session
                user = User.objects.get(id=user_id)  # Ambil user dari model `authentication.models.User`
                event.created_by = user
            except User.DoesNotExist:
                return JsonResponse({'success': False, 'errors': 'User tidak ditemukan.'})

            event.save()
            return JsonResponse({'success': True, 'event_id': event.pk})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    return JsonResponse({'success': False, 'errors': 'Invalid Method'})

@csrf_exempt
def event_edit_flutter(request, pk):
    if 'user_id' not in request.session:
        messages.error(request, "Anda harus login terlebih dahulu.")
        return JsonResponse({'success': False, 'errors': 'Unauthenticated'})

    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        body = json.loads(request.body)
        form = EventForm(body, instance=event)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'event_id': event.pk})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'errors': 'Invalid Method'})

@csrf_exempt
def event_delete_flutter(request, pk):
    if 'user_id' not in request.session:
        messages.error(request, "Anda harus login terlebih dahulu.")
        return JsonResponse({'success': False, 'errors': 'Unauthenticated'})

    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return JsonResponse({'success': True, 'event_id': event.pk})
    return JsonResponse({'success': False, 'errors': 'Invalid Method'})
