from django.db import models
from django.conf import settings
# from forum.models import ForumPost
# from favorites.models import Rating
from authentication.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    food_preferences = models.TextField(blank=True, null=True)
    # forum_posts = models.ManyToManyField(ForumPost, blank=True)  # Menghubungkan ke model ForumPost
    # ratings = models.ManyToManyField(Rating, blank=True)  # Menghubungkan ke model Rating

class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    ingredients = models.TextField()  # Will store ingredients as a string
    steps = models.TextField()        # Will store steps as a string
    image = models.ImageField(upload_to='recipes/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name