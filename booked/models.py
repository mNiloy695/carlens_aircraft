from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
User=get_user_model()

PAYMENT_STATUS=(
    ('held','held'),
    ('refund','refund'),
    ('paid','paid'),
    ('unpaid','unpaid')
)

BOOKING_STATUS=(
    'pending','pending',
    'confirmed','confirmed',
)

class BookedModel(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL)
    operator_id=models.CharField(max_length=100)
    aircraft_id=models.CharField(max_length=100)
    flight_date=models.DateTimeField()
    passengers=models.IntegerField()
    form=models.CharField(max_length=100)
    to=models.CharField(max_length=100)
    amount=models.BigIntegerField()
    currency=models.CharField()
    booking_status=models.CharField(choices=BOOKING_STATUS,default='pending')
    payment_status=models.CharField(choices=PAYMENT_STATUS,default='unpaid')
    

