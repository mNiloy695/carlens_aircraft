from django.db import models

# Create your models here.

PAYMENT_STATUS=(
    ('held','held'),
    ('refund','refund'),
    ('paid','paid'),
    ('upaid','unpaid')
)

class BookedModel(models.Model):
    operator_id=models.CharField(max_length=100)
    aircraft_id=models.CharField(max_length=100)
    flight_date=models.DateTimeField()
    passengers=models.IntegerField()
    form=models.CharField(max_length=100)
    to=models.CharField(max_length=100)
    status=models.CharField()
    