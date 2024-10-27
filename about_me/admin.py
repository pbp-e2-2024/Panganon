from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'food_preferences')
    search_fields = ('user__username', 'bio', 'food_preferences')

admin.site.register(UserProfile, UserProfileAdmin)