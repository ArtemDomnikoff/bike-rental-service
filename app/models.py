from django.db import models
from django.contrib.auth.models import User


class Bike(models.Model):
    bike_id = models.AutoField(primary_key=True)
    bike_model = models.CharField(max_length=100)
    bike_cost = models.DecimalField(max_digits=10, decimal_places=2)
    bike_type = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Bike {self.bike_id} - {self.bike_model} - {self.bike_cost}"


class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    duration = models.DecimalField(max_digits=100, decimal_places=2, null=True)
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('ended', 'Ended')], null=True)

    def __str__(self):
        return f"Rental {self.id} - {self.user.email} - {self.bike.bike_model}"
