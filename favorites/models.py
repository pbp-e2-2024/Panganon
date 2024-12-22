from django.db import models
from authentication.models import User
import uuid
from daftar_toko.models import Restaurant  # Import Restaurant from daftar_toko
    
class FavoriteRestaurant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.restaurant.name} (Favorite: {self.is_favorite})"

class RestaurantReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)