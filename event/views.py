# event/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Event
from .forms import EventForm

def event_list(request):
    events = Event.objects.all()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check if request is AJAX
        event_data = list(events.values())  # Convert to list of dictionaries for JSON response
        return JsonResponse(event_data, safe=False)
    return render(request, 'event/event_list.html', {'events': events})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'event/event_detail.html', {'event': event})

@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return JsonResponse({'success': True, 'event_id': event.pk})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = EventForm()
    return render(request, 'event/event_form.html', {'form': form, 'form_title': 'Create', 'form_button_text': 'Create'})


@login_required
def event_edit(request, pk):
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


@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return JsonResponse({'success': True})
    return render(request, 'event/event_delete_confirmation.html', {'event': event})
