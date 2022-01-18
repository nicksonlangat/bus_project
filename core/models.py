from django.db import models
# Create your models here.
class Bus(models.Model):
    number_plate=models.CharField(
        max_length=10
    )
    start=models.CharField(
        max_length=250
    )
    finish=models.CharField(
        max_length=250
    )
    price = models.FloatField()
    seats=models.IntegerField()
    is_available=models.BooleanField(
        default=True
    )
    def __str__(self) -> str:
        return self.number_plate

class Booking(models.Model):
    STATUS_CHOICES = [ 
    ("Awaiting departure", "Awaiting departure"),
    ("Journey complete", "Journey complete"),
    ("Cancelled", "Cancelled"),
    ]
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    customer = models.CharField(max_length = 150)
    seat=models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    departure=models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length = 20,
        choices = STATUS_CHOICES,
        default = 'Awaiting departure'
        )
    def __str__(self) -> str:
        return self.customer



