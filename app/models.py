from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)


class Bike(models.Model):
    TYPE_CHOICES = [
        ('mountain', 'Mountain'),
        ('city', 'City'),
        ('electric', 'Electric'),
    ]
    id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=100)
    price_per_minute = models.DecimalField(max_digits=6, decimal_places=2)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    is_available = models.BooleanField(default=True)


class Rental(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    duration = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('ended', 'Ended')])

    def __str__(self):
        return f"Rental {self.id} - {self.user.email} - {self.bike.model}"
