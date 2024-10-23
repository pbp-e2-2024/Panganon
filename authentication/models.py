from django.db import models

# Create your models here.
class User(models.Model):
    ROLE_CHOICES = [
        ('adminXYZ123!@#', 'Admin'),
        ('userABC987$%^', 'User'),  
    ]
    
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='userABC987$%^')
    image = models.ImageField(upload_to='photos/', blank=True, null=True)