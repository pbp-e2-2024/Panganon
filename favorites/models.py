from django.db import models
from django.contrib.auth.models import User
import uuid

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    rating = models.FloatField(null=True, blank=True)
    rating_amount = models.IntegerField(null=True, blank=True)
    price_range = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    opening_hours = models.JSONField(null=True, blank=True)
    services = models.JSONField(null=True, blank=True)
    links = models.URLField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class FavoriteRestaurant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

class RestaurantReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'restaurant')   
