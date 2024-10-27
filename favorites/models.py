# favorites/models.py
from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    halal_status = models.CharField(max_length=50, null=True, blank=True)
    operating_hours = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name

class FavoriteRestaurant(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('restaurant',)

class RestaurantReview(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.restaurant.name}"
