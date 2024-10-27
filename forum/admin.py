from django.contrib import admin
from .models import Thread, Post, Comment

class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at')
    search_fields = ('title', 'created_by__username')
    list_filter = ('created_at',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('content', 'thread', 'created_by', 'created_at')
    search_fields = ('content', 'created_by__username', 'thread__title')
    list_filter = ('created_at',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'post', 'created_by', 'created_at')
    search_fields = ('content', 'created_by__username', 'post__content')
    list_filter = ('created_at',)

admin.site.register(Thread, ThreadAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)