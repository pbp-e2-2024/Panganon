from django.contrib import admin
from .models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'date', 'created_by', 'created_at')
    search_fields = ('name', 'location', 'created_by__username')
    list_filter = ('date', 'created_at')
    ordering = ('-date',)

admin.site.register(Event, EventAdmin)