# favorites/models.py
from authentication.models import User
import uuid
from daftar_toko.models import Restaurant  # Import Restaurant from daftar_toko
from django.db import models

class FavoriteRestaurant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True) 
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user','restaurant']

class RestaurantReview(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.restaurant.name}"
