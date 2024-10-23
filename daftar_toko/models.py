from django.db import models

class Makanan(models.Model):
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