from rest_framework import serializers
from .models import *


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['user', 'username', 'email']


class BikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = ['id', 'model', 'price_per_minute', 'type', 'is_available']


class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ['user', 'bike', 'start_time', 'end_time', 'cost', 'duration', 'status']
