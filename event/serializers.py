# event/serializers.py
from rest_framework import serializers
from .models import Event
from authentication.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()  # Nested serialization

    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'location', 'date', 'created_by', 'created_at']