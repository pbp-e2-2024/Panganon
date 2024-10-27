from django.db import models
from authentication.models import User
from datetime import timedelta

class Thread(models.Model):
    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def created_at_plus_7_hours(self):
        return self.created_at + timedelta(hours=7)

class Post(models.Model):
    thread = models.ForeignKey(Thread, related_name='posts', on_delete=models.CASCADE)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def created_at_plus_7_hours(self):
        return self.created_at + timedelta(hours=7)

    def get_top_level_comments(self):
        return self.comments.filter(parent__isnull=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def created_at_plus_7_hours(self):
        return self.created_at + timedelta(hours=7)