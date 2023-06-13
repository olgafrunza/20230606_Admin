from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Flight(models.Model):
    flight_number = models.CharField(max_length=8)
    airlines = models.CharField(max_length=30)
    departure_city = models.CharField(max_length=30)
    arrival_city = models.CharField(max_length=30)
    date = models.DateField()
    time = models.TimeField()
    # datetime = models.DateTimeField()

    def __str__(self):
        return f"{self.date} - {self.time} - {self.departure_city} - {self.arrival_city}"
    
    class Meta:
        ordering = ["date", "time"]
    
class Passenger(models.Model):
    first_name = models.CharField(max_length=50)    
    last_name = models.CharField(max_length=50)    
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Passenger"
        verbose_name_plural = "Passengers"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    flight = models.ForeignKey(Flight, on_delete=models.SET_NULL, null=True, related_name="reservation")
    passenger = models.ManyToManyField(Passenger, related_name="reservations")

    def __str__(self):
        return f"{self.flight} {self.user.username}"