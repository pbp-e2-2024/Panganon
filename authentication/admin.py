from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'role')
    search_fields = ('username', 'name')
    list_filter = ('role',)

admin.site.register(User, UserAdmin)